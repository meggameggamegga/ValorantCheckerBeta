import json
import re
import ssl
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple

import aiohttp
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _extract_tokens(data: str) -> str:
    """Extract tokens from data"""

    pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    response = pattern.findall(data['response']['parameters']['uri'])[0]
    return response


def _extract_tokens_from_uri(url: str) -> Optional[Tuple[str, Any]]:
    try:
        access_token = url.split("access_token=")[1].split("&scope")[0]
        token_id = url.split("id_token=")[1].split("&")[0]
        return access_token, token_id
    except IndexError as e:
        print(f"Cookies Invalid: {e}")


FORCED_CIPHERS = [
    'ECDHE-ECDSA-AES256-GCM-SHA384',
    'ECDHE-ECDSA-AES128-GCM-SHA256',
    'ECDHE-ECDSA-CHACHA20-POLY1305',
    'ECDHE-RSA-AES128-GCM-SHA256',
    'ECDHE-RSA-CHACHA20-POLY1305',
    'ECDHE-RSA-AES128-SHA256',
    'ECDHE-RSA-AES128-SHA',
    'ECDHE-RSA-AES256-SHA',
    'ECDHE-ECDSA-AES128-SHA256',
    'ECDHE-ECDSA-AES128-SHA',
    'ECDHE-ECDSA-AES256-SHA',
    'ECDHE+AES128',
    'ECDHE+AES256',
    'ECDHE+3DES',
    'RSA+AES128',
    'RSA+AES256',
    'RSA+3DES',
]


class ClientSession(aiohttp.ClientSession):
    def __init__(self, *args, **kwargs):
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.minimum_version = ssl.TLSVersion.TLSv1_3
        ctx.set_ciphers(':'.join(FORCED_CIPHERS))
        super().__init__(*args, **kwargs, cookie_jar=aiohttp.CookieJar(), connector=aiohttp.TCPConnector(ssl=False))


class Auth:
    RIOT_CLIENT_USER_AGENT = "ShooterGame/11 Windows/10.0.22621.1.768.64bit"
     #RIOT_CLIENT_USER_AGENT = 'ShooterGame/11 Windows/10.0.22621.1.768.64bit'

    def __init__(self) -> None:
        self._headers: Dict = {
            'Content-Type': 'application/json',
            'User-Agent': Auth.RIOT_CLIENT_USER_AGENT,
            'Accept': 'application/json, text/plain, */*',
        }
        self.user_agent = Auth.RIOT_CLIENT_USER_AGENT

    async def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """This function is used to authenticate the user."""

        session = ClientSession()

        data = {"acr_values": "urn:riot:bronze",
                "claims": "",
                "client_id": "riot-client",
                "nonce": "oYnVwCSrlS5IHKh7iI16oQ",
                "redirect_uri": "http://localhost/redirect",
                "response_type": "token id_token",
                "scope": "openid link ban lol_region"
            }

        r = await session.post('https://auth.riotgames.com/api/v1/authorization', json=data, headers=self._headers)
        cookies = {'cookie': {}}
        for cookie in r.cookies.items():
            cookies['cookie'][cookie[0]] = str(cookie).split('=')[1].split(';')[0]

        data = {"type": "auth", "username": username, "password": password, "remember": True}

        async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data,
                               headers=self._headers) as r:
            data = await r.json()
            for cookie in r.cookies.items():
                cookies['cookie'][cookie[0]] = str(cookie).split('=')[1].split(';')[0]

        await session.close()

        if data['type'] == 'response':
            expiry_token = datetime.now() + timedelta(hours=1)

            response = _extract_tokens(data)
            access_token = response[0]
            token_id = response[1]

            expiry_token = datetime.now() + timedelta(minutes=59)
            cookies['expiry_token'] = int(datetime.timestamp(expiry_token))

            return {'auth': 'response', 'data': {'cookie': cookies, 'access_token': access_token, 'token_id': token_id}}
        else:
            return None

    async def get_entitlements_token(self, access_token: str) -> Optional[str]:
        """This function is used to get the entitlements token."""

        session = ClientSession()

        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}

        async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
            data = await r.json()

        await session.close()
        try:
            entitlements_token = data['entitlements_token']
        except KeyError:
            print('Cookies is expired, plz /login again!')
        else:
            return entitlements_token

    async def get_userinfo(self, access_token: str) -> Tuple[str, str, str]:
        """This function is used to get the user info."""

        session = ClientSession()

        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}

        async with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
            data = await r.json()
        await session.close()
        try:
            puuid = data['sub']
            name = data['acct']['game_name']
            tag = data['acct']['tag_line']
            country = data['country']
        except KeyError:
            print('This user hasn\'t created a name or tagline yet.')
        else:
            return puuid, name, tag,country

    async def get_region(self, access_token: str, token_id: str) -> str:
        """This function is used to get the region."""

        session = ClientSession()

        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}

        body = {"id_token": token_id}

        async with session.put(
                'https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant', headers=headers, json=body
        ) as r:
            data = await r.json()

        await session.close()
        try:
            region = data['affinities']['live']
        except KeyError:
            print('An unknown error occurred, plz `/login` again')
        else:
            return region

    async def give2facode(self, code: str, cookies: Dict) -> Dict[str, Any]:
        """This function is used to give the 2FA code."""

        session = ClientSession()

        data = {"type": "multifactor", "code": code, "rememberDevice": True}

        async with session.put(
                'https://auth.riotgames.com/api/v1/authorization', headers=self._headers, json=data,
                cookies=cookies['cookie']
        ) as r:
            data = await r.json()

        await session.close()
        if data['type'] == 'response':
            cookies = {'cookie': {}}
            for cookie in r.cookies.items():
                cookies['cookie'][cookie[0]] = str(cookie).split('=')[1].split(';')[0]

            uri = data['response']['parameters']['uri']
            access_token, token_id = _extract_tokens_from_uri(uri)

            return {'auth': 'response', 'data': {'cookie': cookies, 'access_token': access_token, 'token_id': token_id}}

        return {'auth': 'failed', 'error': '2FA_INVALID_CODE'}

    async def redeem_cookies(self, cookies: Dict) -> Tuple[Dict[str, Any], str, str]:
        """This function is used to redeem the cookies."""

        if isinstance(cookies, str):
            cookies = json.loads(cookies)

        session = ClientSession()

        if 'cookie' in cookies:
            cookies = cookies['cookie']

        async with session.get(
                "https://auth.riotgames.com/authorize?redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in&client_id=play"
                "-valorant-web-prod&response_type=token%20id_token&scope=account%20openid&nonce=1",
                cookies=cookies,
                allow_redirects=False,
        ) as r:
            data = await r.text()

        if r.status != 303:
            print('COOKIES_EXPIRED')

        if r.headers['Location'].startswith('/login'):
            print('COOKIES_EXPIRED')

        old_cookie = cookies.copy()

        new_cookies = {'cookie': old_cookie}
        for cookie in r.cookies.items():
            new_cookies['cookie'][cookie[0]] = str(cookie).split('=')[1].split(';')[0]

        await session.close()

        accessToken, tokenId = _extract_tokens_from_uri(data)
        entitlements_token = await self.get_entitlements_token(accessToken)

        return new_cookies, accessToken, entitlements_token

    async def temp_auth(self, username: str, password: str) -> Optional[Dict[str, Any]]:

        authenticate = await self.authenticate(username, password)
        if authenticate['auth'] == 'response':
            access_token = authenticate['data']['access_token']
            token_id = authenticate['data']['token_id']

            entitlements_token = await self.get_entitlements_token(access_token)
            puuid, name, tag = await self.get_userinfo(access_token)
            region = await self.get_region(access_token, token_id)
            player_name = f'{name}#{tag}' if tag is not None and tag is not None else 'no_username'

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
                'X-Riot-Entitlements-JWT': entitlements_token,
            }
            user_data = {'puuid': puuid, 'region': region, 'headers': headers, 'player_name': player_name}
            return user_data

        print('TEMP_LOGIN_NOT_SUPPORT_2FA')

    # next update

    async def login_with_cookie(self, cookies: Dict) -> Dict[str, Any]:
        """This function is used to log in with cookie."""

        cookie_payload = f'ssid={cookies};' if cookies.startswith('e') else cookies

        self._headers['cookie'] = cookie_payload

        session = ClientSession()

        r = await session.get(
            "https://auth.riotgames.com/authorize"
            "?redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in"
            "&client_id=play-valorant-web-prod"
            "&response_type=token%20id_token"
            "&scope=account%20openid"
            "&nonce=1",
            allow_redirects=False,
            headers=self._headers,
        )

        # pop cookie
        self._headers.pop('cookie')

        if r.status != 303:
            print('FAILED')

        await session.close()

        # NEW COOKIE
        new_cookies = {'cookie': {}}
        for cookie in r.cookies.items():
            new_cookies['cookie'][cookie[0]] = str(cookie).split('=')[1].split(';')[0]

        accessToken, tokenID = _extract_tokens_from_uri(await r.text())
        entitlements_token = await self.get_entitlements_token(accessToken)

        data = {'cookies': new_cookies, 'AccessToken': accessToken, 'token_id': tokenID, 'emt': entitlements_token}
        return data

    async def refresh_token(self, cookies: Dict) -> Tuple[Dict[str, Any], str, str]:
        return await self.redeem_cookies(cookies)
