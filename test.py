import asyncio
import json
import os
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import aiohttp
import lxml


#--------------ПАРС САЙТА СО СКИНАМИ------------------#
#def main():
#   with open('skins_data_eng.json','r') as file:
#       skins_data = json.load(file)
#   res_skin = {'data':[]}
#   url = 'https://valorantinfo.com/collection/'
#   url_default = 'https://valorantinfo.com/'
#   resp = requests.get(url)
#   data = BeautifulSoup(resp.text,'lxml')
##
#   block = data.find_all('h3',class_='h6 card-title mc-1 m-1 p-1 mt-3 mb-2')
##
#   for coll_url in block:
#       url_collection = url_default + coll_url.find('a').get('href')
#       url_cards = requests.get(url_collection)
#       data_cards = BeautifulSoup(url_cards.text,'lxml')
#       block_card = data_cards.find('div',class_='col-xl-6').find('div',class_='mb-4').find('div',class_='row row-cols-1 row-cols-sm-2 row-cols-lg-3 row-cols-xl-2 row-cols-xxl-2').find_all('div',class_='col text-center')
#       for card in block_card:
#           mini_board = card.find('div',class_='card-ram border-bottom-danger').find('div',class_='small align-items-center text-gray-400 p-2')
##
#           name_skin = card.find('div', class_='card-body p-1').find('h3',class_='h6 card-title mc-1 m-1 p-1 mt-3 mb-2').text.strip()
#           print(f'Скин {name_skin}')
#           price_skin = mini_board.find('div',class_='d-flex').find('div',class_='ml-auto p-2').text.strip()
#           for d in skins_data['data']:
#               if name_skin == d['displayName']:
#                   data_sk = {
#                       'displayIcon':name_skin,
#                       'uuid':d['uuid'],
#                       'vpCost':price_skin
#                       }
#                   res_skin['data'].append(data_sk)
#                   print(f'{name_skin}-{d["uuid"]}-{price_skin} Добавлен!')
#   with open('add_skin.json','w') as file:
#       json.dump(res_skin,file,indent=4)


#async def connecions():
#    async with aiohttp.ClientSession() as s:
#        async with s.get(url=url) as r:
#            page = await r.text()
#            data = BeautifulSoup(page,'lxml')
#            block = data.find_all('h3', class_='h6 card-title mc-1 m-1 p-1 mt-3 mb-2')
#            for coll_url in block:
#                url_collection = url + coll_url.find('a').get('href')
#                print(url_collection)
#
#-----------Скачать фотки------------#
#def main():
#    with open('skins_data.json','r',encoding='UTF8') as file:
#        data = json.load(file)
#    for skin in data['data']:
#        name = skin["displayName"]
#        uuid = skin['uuid']
#        url = skin['displayIcon']
#        if url is None:
#            continue
#        resp = requests.get(url).content
#        photo_name = os.path.exists(fr'photo\{uuid}.jpg')
#        if photo_name:
#            print(f'{name} есть в директории')
#        else:
#            print(f'{name} - Сохранил')
#            with open(f'photo\{uuid}.jpg','wb') as file:
#                file.write(resp)
#
#if __name__=='__main__':
#    main()
#
#--------------------Получить цены скинов---------------------#

import requests

ent_token = 'eyJraWQiOiJrMSIsImFsZyI6IlJTMjU2In0.eyJlbnRpdGxlbWVudHMiOltdLCJhdF9oYXNoIjoiOVZYVmtMVEdzd3BZVU05UnczeEFkUSIsInN1YiI6Ijc0MWMxZDM5LTc4NTAtNWI4Yi1hMjRjLTVjY2ZhNTdjODE5NCIsImlzcyI6Imh0dHBzOlwvXC9lbnRpdGxlbWVudHMuYXV0aC5yaW90Z2FtZXMuY29tIiwiaWF0IjoxNzA3NDMxODQzLCJqdGkiOiJuNjdXa0FJSGUxTSJ9.IwkIhujqiDoRA_L9Zvor4lsBw75cXuVrh--4bR1L6jlrr_AzYngIS3S3LpLJMqyePCEtdEY0QyntxAHdWXBIbbZwqwQRzVn_6VlU1pJXj4mbPwpGRauUi8QZSfR9goo-BOcNChjw6Xj2TfU4ch_-4Xl-b7ykgaNiivoUtN2Je9Fe6ItGVVdvKy60J7A4muAMwOQVxzLM3Fg8YdlyNyPePZeKDVLeTdmKAv_St1C_-wZ17NfLN_I3l1b34VgfiYz0GDVUpGWRDwFOBSfoWk4p0j0vtKJjDszU2xBlQTR6G1eY8FCNmcfMOwmshYPx3IgE1v5FFwL0Ln8bDi7XkaAFeQ'
acc_token = 'eyJraWQiOiJzMSIsImFsZyI6IlJTMjU2In0.eyJwcCI6eyJjIjoiZXUifSwic3ViIjoiNzQxYzFkMzktNzg1MC01YjhiLWEyNGMtNWNjZmE1N2M4MTk0Iiwic2NwIjpbIm9wZW5pZCIsImxpbmsiLCJiYW4iLCJsb2xfcmVnaW9uIiwibG9sIiwic3VtbW9uZXIiLCJvZmZsaW5lX2FjY2VzcyJdLCJjbG0iOlsibG9sX2FjY291bnQiLCJlbWFpbF92ZXJpZmllZCIsIm9wZW5pZCIsInB3IiwibG9sIiwib3JpZ2luYWxfcGxhdGZvcm1faWQiLCJwaG9uZV9udW1iZXJfdmVyaWZpZWQiLCJwaG90byIsIm9yaWdpbmFsX2FjY291bnRfaWQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiLCJsb2NhbGUiLCJiYW4iLCJsb2xfcmVnaW9uIiwiYWNjdF9nbnQiLCJyZWdpb24iLCJwdnBuZXRfYWNjb3VudF9pZCIsImFjY3QiLCJ1c2VybmFtZSJdLCJkYXQiOnsicCI6bnVsbCwibG5rIjpbXSwiYyI6ImVjMSIsImxpZCI6Ik5rb0pXOXhabGRaRFdFTzhxcjF3TmcifSwiaXNzIjoiaHR0cHM6Ly9hdXRoLnJpb3RnYW1lcy5jb20iLCJwbHQiOnsiZGV2IjoidW5rbm93biIsImlkIjoidW5rbm93biJ9LCJleHAiOjE3MDc0MzU0NDMsImlhdCI6MTcwNzQzMTg0MywianRpIjoibjY3V2tBSUhlMU0iLCJjaWQiOiJyaW90LWNsaWVudCJ9.Zc8O-GT203XN1mSnaCIysTOpVnnecKwXsSX3MiuOiAyCHg441i3UymG-0iu_dOvONLwAhJBLPVYGJEc2jn22zIkXHcrjdWNzUymmlrd8giXYMDbv8e0AjV5XEuyY994mcfbVsCHv_yQCyLI4hMtpTCtTWVw7_kKts1FQCFFV5Xc'

headers = {
            "X-Riot-Entitlements-JWT": ent_token,
            "Authorization":f"Bearer {acc_token}"
        }

resp = requests.get('https://pd.eu.a.pvp.net/store/v1/offers',headers=headers)

with open('skins_info/skins_price.json', 'w') as file:
    json.dump(resp.json(),file,indent=4)



#-------------Обновить данные об скинах-------------------#

#import requests
#
#
#
#resp = requests.get('https://valorant-api.com/v1/weapons/skinlevels')
#
#
#with open('skins_data_eng.json','w',encoding='UTF8') as file:
#    json.dump(resp.json(),file,indent=4)














