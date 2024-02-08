import asyncio
import json
import re
import ssl
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple

import aiohttp
import requests
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
    RIOT_CLIENT_USER_AGENT = "ShooterGame/11 Windows/11.0.22621.1.768.64bit"

    def __init__(self) -> None:
        self._headers: Dict = {
            'Content-Type': 'application/json',
            'User-Agent': Auth.RIOT_CLIENT_USER_AGENT,
            'Accept': 'application/json, text/plain, */*',
        }
        self.user_agent = Auth.RIOT_CLIENT_USER_AGENT

    async def authenticate(self, username: str, password: str,proxy=None) -> Optional[Dict[str, Any]]:
        """This function is used to authenticate the user."""
        session = ClientSession()

        data = {
            "client_id": "play-valorant-web-prod",
            "nonce": "1",
            "redirect_uri": "https://playvalorant.com/opt_in",
            "response_type": "token id_token",
            'scope': 'account openid',
        }

        r = await session.post('https://auth.riotgames.com/api/v1/authorization', json=data, headers=self._headers,proxy=proxy)
        cookies = {'cookie': {}}
        print(r.status,'Авторизация')
        for cookie in r.cookies.items():
            cookies['cookie'][cookie[0]] = str(cookie).split('=')[1].split(';')[0]

        data = {"type": "auth", "username": username, "password": password, "remember": True}
        await asyncio.sleep(2)
        async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data,
                               headers=self._headers,proxy=proxy) as r:
            print(r.status,'Добавление куков')
            data = await r.json()#Если 'error':'rate_limited' , то смена прокси
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
        elif data['type'] == 'multifactor':
            return {'type': 'auth', 'error': 'auth_failure', 'country': 'rus'}
        elif data['error'] == 'archived_account':
            return {'type': 'auth', 'error': 'auth_failure', 'country': 'rus'}
        else:
            return data

    async def get_entitlements_token(self, access_token: str) -> Optional[str]:
        """This function is used to get the entitlements token."""

        session = ClientSession()

        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}

        async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
            data = await r.json()
            #print(data)

        await session.close()
        try:
            entitlements_token = data['entitlements_token']
        except KeyError:
            print('Cookies is expired, plz /login again!')
        else:
            return entitlements_token

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

    async def get_userinfo(self, access_token: str) -> Tuple[str, str, str]:
        """This function is used to get the user info."""

        session = ClientSession()

        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {access_token}',
                   'User-Agent':'RiotClient / % s(Windows;10;;Professional, x64'
                   }

        async with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
            data = await r.json()
            print(data,'USER AGENT')

        await session.close()
        try:
            puuid = data['sub']
            name = data['acct']['game_name']
            tag = data['acct']['tag_line']
            email_verif = data['email_verified']
            phone_verif = data['phone_number_verified']
        except KeyError:
            print('This user hasn\'t created a name or tagline yet.')
        else:
            return puuid,name,tag,email_verif,phone_verif

    def get_items(self,item:str,ent_token=None,acc_token=None,region=None,puuid=None):
        headers = {
            "X-Riot-Entitlements-JWT": ent_token,
            "Authorization":f"Bearer {acc_token}"
        }
        #Добавить список items скинов по которым надо сделать запроос
        request = requests.get(
            f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/{item}',
            headers=headers)
        return request.json()
