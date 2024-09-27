import asyncio
import json


def get_proxy(filename='proxy'):
    proxies = []
    with open(r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\other\proxy', 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 3:
                proxy = {
                    'username': parts[0],
                    'password_ip': parts[1],
                    'port': int(parts[2])
                }
                proxies.append(proxy)
    return proxies

        #username = proxy.split()[0]
        #print(username)


def get_skins(items,region,login,password,email,phone):
    with open(r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\skins_info\skins_price.json', 'r') as file:
        prices = json.load(file)
    # ID всех скинов
    with open(r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\skins_info\skins_data_eng.json', 'r', encoding='UTF8') as skins_file:
        skins_data = json.load(skins_file)
    # Словарь для скинов с лвлом
    all_cost = 0
    skin_full = {}
    for skin_id in items['Entitlements']:
        for skin_uuid in skins_data['data']:
            if skin_id['ItemID'] == skin_uuid['uuid']:
                if not 'Level' in skin_uuid['displayName']:
                    skin_full[skin_uuid['displayName']] = skin_uuid['uuid']
                    for price in prices['Offers']:
                        if price['OfferID'] == skin_uuid['uuid']:
                            #print(price['Cost'])
                            all_cost += int(price['Cost']["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"])
    result = f'{login}:{password}|skins:{len(skin_full)}|amount:{all_cost}|region:{region}|email:{email}|phone:{phone}'
    print(result)
    #result = {
    #    login: {
    #        'amount': all_cost,
    #        'countSkins': len(skin_full),
    #        'region': region
    #    }
    #}

    return result


