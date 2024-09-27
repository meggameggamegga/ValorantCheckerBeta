import asyncio
import json
import os
import time
from datetime import datetime

import bs4
import requests
from bs4 import BeautifulSoup
import aiohttp
import lxml


#--------------ПАРС САЙТА СО СКИНАМИ------------------#
#def main():
#   with open('skins_info/skins_data_eng.json','r',encoding='UTF8') as file:
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
#
#main()
#
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
#    with open('skins_info/skins_data.json','r',encoding='UTF8') as file:
#        data = json.load(file)
#    for skin in data['data']:
#        name = skin["displayName"]
#        uuid = skin['uuid']
#        url = skin['displayIcon']
#        if url is None:
#            continue
#        resp = requests.get(url).content# C:\Users\роман\PycharmProjects\valorant_checker_test_v2\src\photos\photo
#        photo_name = os.path.exists(fr'src\photos\photo\{uuid}.jpg')
#        if photo_name:
#            print(f'{name} есть в директории')
#        else:
#            print(f'{name} - Сохранил')
#            with open(f'src\photos\photo\{uuid}.jpg','wb') as file:
#                file.write(resp)
#
#if __name__=='__main__':
#    main()
#
#--------------------Получить цены скинов---------------------#

#import requests
#
#ent_token = 'eyJraWQiOiJrMSIsImFsZyI6IlJTMjU2In0.eyJlbnRpdGxlbWVudHMiOltdLCJhdF9oYXNoIjoiUVc3elVSejVHQWlWY1dEUzgzbm5NQSIsInN1YiI6ImViNTU5YjUxLTRhYzgtNWM0NC1hNWY2LWI5ZjY1ZDM1ODE1NyIsImlzcyI6Imh0dHBzOlwvXC9lbnRpdGxlbWVudHMuYXV0aC5yaW90Z2FtZXMuY29tIiwiaWF0IjoxNzA5OTMyNTM4LCJqdGkiOiJKWHpsTU9GWFF4MCJ9.GqTnxGMDendIo3w3jZfrbrhLkMwq8pEnd1dr6Rjx5SQxAaRrjqeMI9piaX9iKLJLfVYyV8J6AI8CqHNjVqMO-XhpVgOmp3iYf9xZEmYEZpkeyRVbyYIcK8ZETBqBTTKpp_Uaiu_jzEIJ-1Wo4LXqCZcU4f2YfNXo6eFjPfT3JGI-BzCVsemdJxbqy6poPOMQGL9x1jlZui9LY45qcc39f3Z5hUQyfl7lKOiRCaaEhvUfG8AujWIjyp4W7JpYmZFRNaO0Wu-dMyOGBWkQQh7H7atU8sIivzTh7Wp5MCjXJ-DCMJHpXYT8WQELH9wEBpaJYCMhYBYH8z0y9x1HGJFw-A'
#acc_token = 'eyJraWQiOiJzMSIsImFsZyI6IlJTMjU2In0.eyJwcCI6eyJjIjoiZXUifSwic3ViIjoiZWI1NTliNTEtNGFjOC01YzQ0LWE1ZjYtYjlmNjVkMzU4MTU3Iiwic2NwIjpbIm9wZW5pZCIsImxpbmsiLCJiYW4iLCJsb2xfcmVnaW9uIiwibG9sIiwic3VtbW9uZXIiLCJvZmZsaW5lX2FjY2VzcyJdLCJjbG0iOlsicmduX0VVTjEiLCJsb2xfYWNjb3VudCIsImVtYWlsX3ZlcmlmaWVkIiwib3BlbmlkIiwicHciLCJsb2wiLCJvcmlnaW5hbF9wbGF0Zm9ybV9pZCIsInBob25lX251bWJlcl92ZXJpZmllZCIsInBob3RvIiwib3JpZ2luYWxfYWNjb3VudF9pZCIsInByZWZlcnJlZF91c2VybmFtZSIsImxvY2FsZSIsImJhbiIsImxvbF9yZWdpb24iLCJhY2N0X2dudCIsInJlZ2lvbiIsInB2cG5ldF9hY2NvdW50X2lkIiwiYWNjdCIsInVzZXJuYW1lIl0sImRhdCI6eyJwIjpudWxsLCJyIjoiRVVOMSIsImMiOiJ1dzEiLCJ1IjoyMTYxODM5NzUwMDgyNzUyLCJsaWQiOiJTRmRrUElFQXVrQUpoYnBCNnNNTGZBIiwibG5rIjpbXX0sImlzcyI6Imh0dHBzOi8vYXV0aC5yaW90Z2FtZXMuY29tIiwicGx0Ijp7ImRldiI6InVua25vd24iLCJpZCI6InVua25vd24ifSwiZXhwIjoxNzA5OTM2MTM3LCJpYXQiOjE3MDk5MzI1MzcsImp0aSI6IkpYemxNT0ZYUXgwIiwiY2lkIjoicmlvdC1jbGllbnQifQ.MHDZMbUZHhdJ2bvr8galiTvsiulvqkQmQOsLm-RVLsAPyzqhn_MygmPtXpDisGfUVnBpSsjnYL___-vk_77PFBGDi8bKtqD41IuB7VWH2XHC4ei_TqscWgBod8b_riM48S9tPk5d178AutLjkQaB_WJ3YU44hB6oRs6cCMWMMvk'
#
#headers = {
#            "X-Riot-Entitlements-JWT": ent_token,
#            "Authorization":f"Bearer {acc_token}"
#        }
#
#resp = requests.get('https://pd.eu.a.pvp.net/store/v1/offers',headers=headers)
#
#with open('skins_info/skins_price.json', 'w') as file:
#    json.dump(resp.json(),file,indent=4)



#-------------Обновить данные об скинах-------------------#

#import requests
#
#
#
#resp = requests.get('https://valorant-api.com/v1/weapons/skinlevels?language=ru-RU')
#
#
#with open('skins_info/skins_data.json','w',encoding='UTF8') as file:
#    json.dump(resp.json(),file,indent=4,ensure_ascii=False)


#--------------------Добавить фотки новой колекции-----------------#

#def add_collection_photo(name):
#    with open('skins_info/skins_data.json','r',encoding='UTF8') as file:
#        data = json.load(file)['data']
#
#    for skin in data:
#        if name in skin['displayName']:
#            try:
#                resp = requests.get(skin['displayIcon']).content
#                with open(f'tst/{skin["uuid"]}.jpg','wb') as file:
#                    file.write(resp)
#                print(f'Добавил {skin["displayIcon"]}')
#            except:
#                pass
#add_collection_photo('Sovereign')

#



#-----------Добавить скины в колекцию--------------------#
#def add_name_in_coll(name_coll):
#    with open('skins_info/skins_data.json','r',encoding='UTF8') as file:
#        data = json.load(file)['data']
#
#    with open('skins_info/collections_tier.json','r',encoding='UTF8') as file:
#        data_cl = json.load(file)
#    for skin in data:
#        if name_coll in skin['displayName']:
#            if 'нож' in skin['displayName']:
#                data_cl['EXCLUSIVE'].append(skin['displayName'])
#                print('Добавил 1')
#            else:
#                data_cl['DELUXE'].append(skin['displayName'])
#                print('Добавил')
#        with open('skins_info/collections_tier.json', 'w', encoding='UTF8') as file:
#            json.dump(data_cl, file, indent=4, ensure_ascii=False)
##

#add_name_in_coll('Либерти')


#with open('other/proxy','r') as file:
#    data = file.readlines()
## 181.168.93.14 4153
#for proxy in data:
#
#    log = proxy.split(':')[0]
#    password_ip = proxy.split(':')[1]
#    port = proxy.split(':')[2]
#
#    proxies = {
#        'http':f'http://172.67.11.138:80',
#        'https':f'https://172.67.11.138:80'
#    }
#
#    resp = requests.get('https://icanhazip.com/',proxies=proxies).text
#
#    print(resp)



#def main():
#    urls = ['https://valorantinfo.com/ru/collection/primordium',
#            'https://valorantinfo.com/ru/collection/jellyfish',
#            'https://valorantinfo.com/ru/collection/jetski',
#            'https://valorantinfo.com/ru/collection/shellfish',
#            'https://valorantinfo.com/ru/collection/tarot']
#    url = 'https://valorantinfo.com/ru/collection/primordium'
#
#    resp = requests.get(url)
#    data = bs4.BeautifulSoup(resp.text,'lxml')
#
#    block_skins = data.find('div',class_='row row-cols-1 row-cols-sm-2 row-cols-lg-3 row-cols-xl-2 row-cols-xxl-2').find_all('div',class_='col text-center')
#    print(block_skins)
#
#if __name__ == '__main__':
#    main()
#
#
#with open('accs.txt', 'r') as file:
#    data = file.readlines()
#
#
#with open('new_accs.txt','a') as file:
#    for i in data:
#        info = i.split(' ')
#        log_pass = info[2]
#        file.writelines(log_pass)

