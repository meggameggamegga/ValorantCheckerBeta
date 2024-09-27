from valo_lib import Auth

import requests

regions = ['latam', 'br', 'na']


class ClientAcc:
    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password
        self.cookie = None
        self.access_token = None
        self.token_id = None
        self.entitlements_token = None
        self.puuid = None
        self.name = None
        self.tag = None
        self.region = None
        self.player_name = None
        self.country = None

    async def autheticate(self):
        auth = Auth()
        authenticate = await auth.authenticate(self.username, self.password)
        # Если ответ произошел
        if not authenticate:
            return None
        else:
            if authenticate['auth'] == 'response':
                auth_data = authenticate['data']
                self.cookie = auth_data['cookie']['cookie']
                self.access_token = auth_data['access_token']
                self.token_id = auth_data['token_id']
                self.entitlements_token = await auth.get_entitlements_token(self.access_token)
                self.puuid, self.name, self.tag, self.country = await auth.get_userinfo(self.access_token)
                self.region = await auth.get_region(self.access_token, self.token_id)
                if self.region in regions:
                    self.region = 'na'
                self.player_name = f'{self.name}#{self.tag}' if self.tag is not None and self.name is not None else 'no_username'
                return {'access_token': self.access_token, 'token_id': self.token_id,
                        'entitlements_token': self.entitlements_token,
                        'puuid': self.puuid, 'name': self.name, 'tag': self.tag, 'region': self.region,
                        'player_name': self.player_name}
            else:
                return False

    # ---------------Получить нужные вещи-----------------#
    def get_items(self, item: str, ent_token=None, acc_token=None, region=None, puuid=None):
        headers = {
            "X-Riot-Entitlements-JWT": ent_token,
            "Authorization": f"Bearer {acc_token}"
        }
        # Добавить список items скинов по которым надо сделать запроос
        request = requests.get(
            f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/{item}',
            headers=headers)

        return request.json()

    def get_store(self, ent_token=None, acc_token=None, region=None, puuid=None):
        headers = {
            'X-Riot-ClientVersion': "release-08.03-shipping-11-2301612",
            # "release-08.00-shipping-14-2191955", #"release-07.06-shipping-4-983570",
            "X-Riot-Entitlements-JWT": ent_token,
            "Authorization": f"Bearer {acc_token}"
        }

        request = requests.get(
            url=f'https://pd.{region}.a.pvp.net/store/v2/storefront/{puuid}',  # region,puuid,code_items
            headers=headers)
        return request.json()

    def get_mathes(self, ent_token=None, acc_token=None, region=None, puuid=None):
        headers = {
            'Content-Type': 'application/json',
            "X-Riot-Entitlements-JWT": ent_token,
            "Authorization": f"Bearer {acc_token}"
        }

        request = requests.get(
            url=f'https://pd.{region}.a.pvp.net/match-history/v1/history/{puuid}',
            headers=headers)
        return request.json()

    # "LatestCompetitiveUpdate""TierAfterUpdate" or  '"CompetitiveTier"'
    def get_my_account(self, ent_token=None, acc_token=None, region=None, puuid=None):
        headers = {
            'Content-Type': 'application/json',
            "X-Riot-Entitlements-JWT": ent_token,
            "Authorization": f"Bearer {acc_token}"
        }
        # Получить баланс игрока
        request = requests.get(
            url=f'https://pd.{region}.a.pvp.net/store/v1/wallet/{puuid}',
            headers=headers)
        try:
            VP = request.json()['Balances']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
            Kingdom = request.json()['Balances']['85ca954a-41f2-ce94-9b45-8ca3dd39a00d']
            RP = request.json()['Balances']['e59aa87c-4cbf-517a-5983-6e81511be9b7']
        except:
            VP = None
            Kingdom = None
            RP = None

        headers = {
            'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9',
            'X-Riot-ClientVersion': "release-08.04-shipping-4-2324912",
            # release-08.03-shipping-11-2301612(prev_new) "release-08.00-shipping-14-2191955"
            'X-Riot-Entitlements-JWT': ent_token,
            'Authorization': f'Bearer {acc_token}'
        }

        request = requests.get(
            url=f'https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}',
            headers=headers).json()
        competitive = request["QueueSkills"]['competitive']

        count_games_for_rating = competitive["TotalGamesNeededForRating"]

        # Если нет звания
        if int(count_games_for_rating) > 0:
            rank = 0  # То есть у него нет ни одной игры
            last_match = request["LatestCompetitiveUpdate"]
            # Если есть крайний матч, то берем крайнюю игру
            if last_match is not None:
                time_last_match = last_match.get("MatchStartTime")
                # formatted_time = datetime.fromtimestamp(time_last_match / 1000).strftime('%Y-%m-%d %H:%M:%S')
            else:  # Если нет крайней игры,то ставим нет крайней игры
                time_last_match = None
                # formatted_time = None
            return {'VP': VP, 'Kingdom': Kingdom, 'RadiantPoints': RP, 'Rank': rank, 'last_match': time_last_match}


        else:  # Если есть звание
            # Тут сверить сезоны , может и не быть игры в новом сезоне, то выдавать с крайнего матча
            try:
                rank = competitive["SeasonalInfoBySeasonID"]["22d10d66-4d2a-a340-6c54-408c7bd53807"].get(
                    "CompetitiveTier")
            except:
                rank = 0
            last_match = request["LatestCompetitiveUpdate"]["MatchStartTime"]
            # formatted_time = datetime.fromtimestamp(last_match / 1000).strftime('%Y-%m-%d %H:%M:%S')
            return {'VP': VP, 'Kingdom': Kingdom, 'RadiantPoints': RP, 'Rank': rank, 'last_match': last_match}

        #    #formatted_time = datetime.fromtimestamp(last_match / 1000).strftime('%Y-%m-%d %H:%M:%S')
        #    return {'VP':VP,'Kingdom':Kingdom,'RadiantPoints':RP,'Rank':rank,'last_match':last_match}
        # except Exception as e:
        #    rank = request.json()['QueueSkills']["competitive"]["TotalGamesNeededForRating"]
        #    try:
        #        last_match = request.json()['LatestCompetitiveUpdate']['MatchStartTime']
        #        print(last_match)
        #        #formatted_time = datetime.fromtimestamp(last_match / 1000).strftime('%Y-%m-%d %H:%M:%S')
        #        return {'VP': VP, 'Kingdom': Kingdom, 'RadiantPoints': RP, 'Rank': None, 'last_match': last_match,'games': rank}

    #
    #    except Exception as e:#Если нет звания и нет крайнего матча вообще то попадает сюда
    #        last_match ='Рейтинг не открыт'
    #        return {'VP': VP, 'Kingdom': Kingdom, 'RadiantPoints': RP,'Rank':None,'last_match': last_match,'games':rank}

    def get_agents(self, ent_token=None, acc_token=None, region=None, puuid=None):
        headers = {
            'X-Riot-ClientVersion': "release-08.04-shipping-4-2324912",  # "release-08.00-shipping-14-2191955",
            "X-Riot-Entitlements-JWT": ent_token,
            "Authorization": f"Bearer {acc_token}"
        }
        responce = requests.get(
            url=f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/01bb38e1-da47-4e6a-9b3d-945fe4655707',
            headers=headers)
        return responce.json()

    def check_verif(self, acc_token):
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {acc_token}"
        }
        responce = requests.get('https://auth.riotgames.com/userinfo', headers=headers)
        return responce.json()

    def get_breloki(self, ent_token=None, acc_token=None, region=None, puuid=None):
        headers = {
            "X-Riot-Entitlements-JWT": ent_token,
            "Authorization": f"Bearer {acc_token}"
        }
        responce = requests.get(
            url=f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/dd3bf334-87f3-40bd-b043-682a57a8dc3a',
            headers=headers)
        return responce.json()

    async def start(self):
        return await self.autheticate()

# async def main():
#    client = ClientAcc(username='username',password='passowrd')
#    await client.start()
#
#
# if __name__=='__main__':
#    asyncio.run(main())
