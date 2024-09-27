# Определите путь к папке с изображениями
import json
import os
import logging
from PIL import Image, ImageDraw, ImageFont


def image_skins(lang):
    skin_full = {'Shorty "Вундеркинд"': 'f9688e62-42c5-9f10-f160-49abaee2e02c', 'Sheriff "Странник"': 'b9bf9657-411e-8fe3-b717-b99ba01fe07a', 'Frenzy "Демон"': '4add59eb-41f6-4184-3cb6-c89a81b6739b', 'Spectre "Винил"': '6803ed34-46cc-ba84-9e58-f78f6538151e', 'Онимару Куницуна': '901abab9-4a44-09f1-b892-9887a587f079', 'Sheriff "Конец игры"': '443f5a29-4d5e-d63e-a3c6-ada7713172fa', 'Stinger "Гроза оборотней"': '7ffbef55-4108-945e-6bc9-7b897f386d1b', 'Bulldog "Radiant Entertainment System"': '7deb8bd7-4ff6-64d2-1f23-2fb7143a5d98', 'Нож "Боец"': '21d49b4a-49ce-79f9-4e08-67959f8d17b5', 'Judge "Аквапринт"': '2a25f841-4769-6536-ded3-8890ee26c430', 'Bucky "Аквапринт"': '338bb3e6-4c47-425d-32a5-5ea1a96c78ae', 'Judge "Усмиритель"': '2d535295-4ad0-bcb1-1ab7-b8b0617a9abc', 'Frenzy "Коалиция: Кобра"': '337b4e6a-46d8-8359-50c0-388717617044', 'Bulldog "Демон"': '94456e3a-459f-4447-cc0d-7e9b5d01b81e', 'Vandal ".SYS"': 'e9953add-4069-d71b-447a-a8ad94fe6526', 'Ghost "Либретто"': '975b222c-430d-b59a-71b7-7cac1461b276', 'Bulldog "Боец"': '842dbe37-4bc7-95b3-26d7-a0af65615d5e', 'Shorty "Завиток"': '10cf91e9-4902-3898-3857-b4ad13882e71', 'Vandal "Нептун"': '49cea67c-4552-13c2-6b4b-8ba07761504e', 'Sheriff "Новый фронтир"': 'd9f04b7a-4ca6-1083-3af4-e3810bf15440', 'Stinger "Схема"': '0329743b-4ce8-be9f-b531-f4aadc890287', 'Stinger "Конструктор"': 'd9b038d8-4f8c-e4a6-e538-6e9cfb0dbb11', 'Веер "Пламя"': '445de3d7-4833-5bf7-ef75-aeb4a0212229', 'Phantom "Скорость"': '4707bae8-4938-71b5-ce5c-52aad3f24d21', 'Bulldog "Перелив"': '49b2e3c2-447c-7aba-ca50-a8993a72d969', 'Bulldog "Винил"': '9db51105-45a7-d05e-6d7d-08962c65c386', 'Stinger "Либретто"': 'bf4bee28-45f5-a512-5ccc-3284ad7ba59a', 'Classic "Усмиритель"': '60f3166c-4a22-9d8c-519a-f09b5fa1416b', 'Vandal "Город монстров"': 'eaf52d49-4608-45d9-5f18-c8b12614e01f', 'Phantom "Конструктор"': '0d203d6e-4944-7341-5f43-46a563b084c5', 'Vandal "Демон"': '9246f649-40b1-4077-31d1-be856acf5dd9', 'Frenzy "Под напряжением"': '08e6ba32-4a6e-8680-df58-39af9c32cdac', 'Frenzy "РагнаРокер"': 'b02520dd-48cd-466c-977d-529dc6a1d6f5', 'Sheriff "Империум"': 'e63cee8f-47b4-1d3d-6eb2-5b9a59f1aa2a', 'Frenzy "Фуксия"': '7b04cfc0-4c93-3bcb-7f3a-e189611412e3', 'Frenzy "Аквапринт"': 'c485b3df-4ea3-d457-e75b-35add7e78e7e', 'Marshal "Конструктор"': 'b878ea87-4383-caeb-ce4b-f7a37f42bb02', 'Odin "Коалиция: Кобра"': 'dd2acfca-4366-7ac0-c13e-1eb2f1948273', 'Ghost "Radiant Entertainment System"': 'b0c41f3b-4fa8-3768-4436-a29fbef94a68', 'Посох руи': 'dd587e30-4932-6cd4-3437-a1a043dd6a78', 'Bucky "Панорама"': '7f56c527-4185-be0e-a0ea-18b31a781c90', 'Guardian "Аквапринт"': '0ab465ed-4539-16f1-b791-5384280e0a1c', 'Classic "Мастерство"': '30f3e881-43d0-a455-b272-e8968c45761f', "Ares ''Небесная свинка''": '75e66837-47b4-0aec-cf8e-8b96f3af7d6b', 'Ghost "Гроза оборотней"': '04c6f57c-4463-f8b7-a475-6c89b2ec4416', 'Ghost "Звездная одиссея"': '0235ff00-4ba4-2092-ea7d-b99299d7017f', "Judge ''Небесная свинка''": '7ae57ece-4560-236b-5bdb-5f8ee2c294b2', 'Ares "Силуэт"': 'ba8b956f-4856-4946-9ae0-248201f1ed9e', 'Sheriff "Конструктор"': '77445d85-4b8a-3008-f98e-c3a42f72044a', 'Sheriff "Бессмертие"': 'd3f40fb9-40ec-b61f-7479-ceaded7b176a', 'Operator "Radiant Entertainment System"': '722a1311-43e1-7c18-ce90-acac33e9c2ad', 'Phantom "Чаропанк"': '82da0235-41c6-4a04-8296-e9baaa8f12a0', 'Кунай "Champions\xa02023"': '19c97db0-4ea8-d0de-d2a9-398eecb07298', 'Stinger ".SYS"': '50e072a5-4f30-63a9-6dee-a8b33781269f', 'Guardian "Лунная битва"': 'c04a92d3-445a-1d3c-07fb-99ba9637c0bd', "Marshal ''Небесная свинка''": '3711156a-43c5-de94-3ccc-ee8bae5e6df0', 'Bulldog "Усмиритель"': 'ae2bac38-48c3-a8b0-e843-eea29fab477b', 'Vandal "Стражи света"': '968efd06-4549-65f4-9fb1-3f90d612e428', 'Sheriff "Защитник"': 'd9fc55c6-4b92-98ac-5052-2a8b5ca4fb71', 'Vandal "Гроза оборотней"': 'f158e7d9-4404-1e88-747e-bf98da9a744b', 'Judge "Цифровая магия"': '64f5eaef-434b-69c5-5014-36a58ec1de20', 'Frenzy "Лунная битва"': '205449a6-45b6-e045-fe74-b09e9cc6d713', 'Vandal "Перелив"': '3c64689e-4bee-6e6e-8681-fdb9ee6b110f', 'Bulldog "Либретто"': 'bd7c039b-4ccc-1a20-acbf-dda25431e350', 'Bulldog "Цифровая магия"': 'c58376cc-41f8-ba0b-c42d-319b135ab994', 'Vandal "Чаропанк"': 'a0801408-4a88-3bc7-df50-0baaecf5040b', 'Judge "Коалиция: Кобра"': 'fe644484-4d07-5472-9e4a-d3992f2f2ecb', 'Marshal "Лунная битва"': 'f92d4bee-43a0-76e0-b07a-e6a064749617', 'Нож "Перелив"': '45159daa-423b-200a-c043-babdec9d0fd8', 'Vandal "Ион"': 'a8c10620-46a8-794e-be55-a0a13edb8d44', 'Bulldog "Скорость"': '7561a8e0-4cc4-8644-a88b-48a88790b36f', 'Operator "Либретто"': 'd3b378f7-4276-a4b5-2ef4-45a580c0ced6', 'Operator "Фуксия"': '93f788fa-4fb5-b372-ce71-b6b413ce0902', 'Ghost "Мастер"': 'b70db444-4ede-9cee-25dd-35b2edb38cd5', 'Sheriff "Город монстров"': 'f3d205b2-4975-3688-6613-039648e3a226', 'Ghost "Фрихэнд"': '21f136ee-4fd6-22dd-56c9-a9869ef31dda', 'Frenzy "Бросок"': '2f911f78-46e4-102a-f677-37a069c3a4dc', 'Искра "Чаропанк"': '35792a19-4e62-f3bc-f5df-289599d6cafc', 'Frenzy "Полет"': '2f69bfe0-4126-4d2b-91b4-c9a2cb1909da', 'Classic "9\xa0жизней"': 'b2ae014f-4c4e-1308-d1c7-e8bc70c46947', 'Marshal "Фрихэнд"': '30240598-46fb-8f6d-4923-1c957f468718', 'Ares "Отважный герой"': '6ab209eb-4596-c1f5-0262-22ac9f2beaa0', 'Operator "Отважный герой"': 'a7ec8cbf-499b-31cc-d58f-a2a900d7239c', 'Равновесие': 'ef67d6cb-4f7f-28ce-2973-cf90a97ae54d', 'Operator "Боец"': '3cd5ed19-405b-9600-489f-4e84900ea2d3', 'Guardian "Панорама"': 'a8c576f3-4c82-f631-6d2d-9fb99f2053fa', 'Stinger "Лунная битва"': 'b50b4766-492d-56b0-0bc3-bea6eba2606d', 'Spectre "Боец"': '6c69c2bc-4c7a-6308-8384-a1b2aa00a50b', 'Ghost "Вендетта"': '4526a891-4754-da6c-7ada-95a8a259952e', 'Judge "Империум"': '4f44cdaa-4810-efd2-0531-5d9565a4ec39', 'Sheriff "Схема"': 'b5601f65-4467-7946-8a37-45bed5514f98', 'Operator "Империум"': '176e6fa8-472d-9eb1-a474-11a3080c4053', 'Холодное оружие ".SYS"': '9d9ec56d-4973-3531-64f5-6d8eb2beb0a2', 'Odin "Гроза оборотней"': 'e1a05cb4-4ac5-b15a-e86e-bab0f7e093ad', 'Sheriff ".SYS"': '6287a1f1-4d10-5190-86ec-659b26020e87', 'Marshal "Песчаная буря"': '3296826f-4973-d5e1-e360-548ba5598faf', 'Frenzy "Силуэт"': '7dee6b38-400a-c9a4-3bac-cb87876e2873', 'Classic "Боец"': '564806a9-43fd-986e-7901-6790b6077a0d', 'Spectre "Фрихэнд"': '607e86c7-4ddf-4fa7-4fdb-c5a6013a90f8', 'Vandal "Отважный герой"': 'c8931118-40b7-dfb6-c071-85be21d51b4d', 'Ghost "Цифровая магия"': '9e0cfab0-428d-8eba-c554-ebac2614e43f', 'Judge "Силуэт"': '89af4c8b-4649-d61a-e1c3-fe95a90bae6a', 'Bucky ".SYS"': 'b7652717-49c0-b658-529e-6f8146ab0eca', 'Ghost "Отважный герой"': '604fa485-43ba-0fcf-4bad-f9a4e3b6c652', 'Vandal "Champions\xa02023"': '69f94fda-4603-744a-87fe-2391be7462e8', 'Клинок "Империум"': '1d7449fe-4bba-e213-c0c2-39816ca1043f', 'Spectre "Скорость"': '5172ea04-432f-2bfb-2163-808ccc2442c3', 'Vandal "Прайм"': 'c9678d8c-4327-f397-b0ec-dca3c3d6fb15', 'Shorty "Скорость"': 'c6db7920-4d61-556e-7c06-19954b847cbe', 'Marshal "Коалиция: Кобра"': '4dd7d0b9-40a9-de6c-ac61-aea19a6d8a77', "Frenzy ''Небесная свинка''": 'e44b70cf-4e83-19d3-a748-5f849054dad7', 'Odin "Фрихэнд"': '7d9adf46-48c5-9247-7121-1ba9e328e70c', 'Shorty "Змеиный укус"': '6f90d1ed-4acc-d925-4a8a-60913f14d16b', 'Керамбит "Скорость"': 'c01062ab-48ed-11a2-46bb-dba096daca59', 'Shorty "Винил"': '31629ef7-47ac-908e-369b-16beabc02c5b', 'Classic "Последняя надежда"': 'bbbe4b32-457c-e4fb-a674-1d9c3885d331', 'Power Fist': 'f2090053-4392-37bf-18bc-e7a03c1ebd82', 'Phantom "Прайм//2.0"': '9dc0bdd7-4d88-9360-38d6-3ea62b1daaca', 'Phantom "Radiant Entertainment System"': '28a7fd58-425c-6aa7-40d6-539d5fdac46c', 'Spectre "Песчаная буря"': '288073b8-4b6d-cef3-cbbe-49bb21670090', 'Phantom "Радиояд"': '21e0eb12-4211-3346-f01b-7b82c7931320', 'Усмиритель ': '76722e7d-4a64-a76e-98a7-0b9ec7d107e2', 'Shorty "Перелив"': '42a5b584-468b-0812-3041-7cb8b36cc0f8', 'Ghost "Тихарь"': 'afcb2528-4415-0178-98b1-c0a751092762', 'Vandal "Империум"': '43e7b969-4d2b-6d7b-6430-81bb37767481', 'Odin "Схема"': '15a5516d-412f-2db0-6bb3-3cbe40a2355f', 'Ares "Демон"': '8b829b66-44ad-c5d3-4e03-f5bc3c6f5d12', 'Ares "Город монстров"': 'de269cd5-448a-7374-db37-ad8e54a4d70d', 'Vandal "Араксис"': 'a3dba920-44ee-d7c5-5227-99a80aee3bd9', 'Vandal "Жнец"': 'ba42fe63-457a-78ce-4499-47950a698129', 'Spectre "Фуксия"': 'f3e9786c-44f4-712e-8033-c99c90d55e1b', 'Classic "Панорама"': 'd8bf97ac-4bc6-4896-1ca0-48b6545a64ab', 'Guardian "Фуксия"': '80fd2b3e-4854-204b-718d-aeaaeb5b63a5', 'Vandal "Схема"': '76c30002-4884-8193-dcf6-93a00b10bc15', 'Ares "Цифровая магия"': 'cba40da2-40b5-7f53-14f8-60a82bcdeee8', 'Ghost "Жнец"': 'a6fe7710-4edc-5e23-223d-aeaef3d17866', 'Stinger "Перелив"': '066522e1-4d71-d514-2943-70a1df85badf', 'Нож "Конструктор"': '54aa7ea7-4839-65b3-e0a8-d6a6aeb945fd', 'Phantom "Усмиритель"': 'efd31e00-4a50-2b1d-e27f-dfa5bc9687f2', 'Нож "VALORANT GO! Вып. 1"': '6e37a33a-416e-fcc0-ceb8-7784e18fbfe9', 'Spectre "Город монстров"': '700e2ea1-474a-c575-1957-88a038e61982', 'Ghost "Монарх"': 'ed8a1109-4e48-f077-636b-e98dd332bfcc', 'Vandal "Предвестник хаоса"': '1010fb40-4344-6ec8-2a8a-33bf076339b6', 'Ghost "Головоломка"': 'd0793c86-471d-c60c-b0da-bcbadcd8bf12'}
    links = []
    images_folder = 'photo'
    # Определите размер фонового изображения
    background_width = 700
    background_height = 1000
    # Определите путь к папке, в которой нужно сохранить созданные фоны
    output_folder = f'accept_photo/'
    # Создайте пустой фон
    background = Image.new('RGBA', (background_width, background_height), (250, 244, 224))  # 0,0,0,255
    # Создайте объект ImageDraw для добавления текста
    draw = ImageDraw.Draw(background)
    # Задайте шрифт и размер текста
    font = ImageFont.truetype("arial.ttf", 40)
    # Задайте текст и его позицию
    text = "@checker_valo_bot"
    text_position = (150, background_height - 100)
    # Нарисуйте текст на изображении
    draw.text(text_position, text, fill=(0, 0, 0, 255), font=font)
    # Определите отступы для вставки изображения
    x_offset = 15
    y_offset = 15
    # Максимальное количество изображений на одном фоне
    max_images_per_background = 35
    current_image_count = 0
    # Список для хранения всех созданных фонов
    backgrounds = []
    names_default = ['Odin', 'Sheriff', 'Ghost', 'Stinger', 'Marshal', 'Spectre', 'Shorty', 'Guardian', 'Classic',
                     'Frenzy', 'Bulldog', 'Ares', 'Judge', 'Bucky']
    # Пройдитесь по данным и вставьте изображения на фон
    for k, url in skin_full.items():
        if lang == 'EU':
            try:
                name = k.split(' ')[1]
            except Exception as e:
                pass
        else:
            name = k.split(' ')[0]  # Для EN
        try:
            if url:
                # Полный путь к файлу
                image_path = os.path.join(images_folder, f'{url}.jpg')#
                # Проверка наличия файла
                if os.path.exists(image_path):
                    image = Image.open(image_path).resize((100, 55))  # Скин картиинка
                    coll_photo = make_collection(name=k)
                    if coll_photo:
                        image_with_background = Image.new('RGB', (120, 110), (255,255,255))#Это самое заднее
                        #Это коллекция
                        image_collection = Image.open(fr'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\collection_photo\{coll_photo}.jpg').resize((110,50)) # Белый фон, если скин не найден
                        image_with_background.paste(image_collection,(5,10),image_collection)#Это коллекция
                        image_with_background.paste(image,(4,50),image)#Это скин
                        #image_collection.paste(image_with_background,(5,10),image_with_background)#Двигается image_collection по image_with_back
                    else:
                        background_color = (1,1,1,1)
                        image_with_background = Image.new('RGB', (120, 110), background_color)#Это фон с коллекцией
                        image_with_background.paste(image, (5, 20), image) #Это вставка и коорди
                    # Пишем имя скина
                    draw_name_skin = ImageDraw.Draw(image_with_background)
                    font_name = ImageFont.truetype("arial.ttf", 11)
                    text_skin = k  # Название скина из переменной k
                    text_position_skin = (1, 1)  # Позиция текста (x, y) на изображении
                    text_color = (0, 0, 0, 255)  # Цвет текста (черный)
                    draw_name_skin.text(text_position_skin, text_skin, fill=text_color, font=font_name)
                    # Вставьте изображение на фон с указанными отступами
                    background.paste(image_with_background, (x_offset, y_offset))
                    # Обновите отступы для следующего изображения
                    x_offset += image_with_background.width + 10
                    current_image_count += 1
                    # Если x_offset превышает ширину фона
                    if x_offset + image_with_background.width > background_width:
                        x_offset = 15
                        y_offset += image_with_background.height + 10
                    if current_image_count >= max_images_per_background:
                        x_offset = 15
                        y_offset = 15
                        current_image_count = 0
                        # Сохраните текущий фон в список backgrounds
                        backgrounds.append(background.copy())
                        # Создайте новый фон
                        background = Image.new('RGBA', (background_width, background_height), (250, 244, 224))
        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")

    # Сохраните оставшийся текущий фон
    backgrounds.append(background)
    # Закройте фоны
    for i, bg in enumerate(backgrounds):
        # Создайте имя файла с уникальным именем (например, background_1.png, background_2.png и т. д.)
        output_path = os.path.join(output_folder, f'background_{i + 1}.png')  # label
        bg.save(output_path)
        links.append(output_path)
    # Закройте фоны
    for bg in backgrounds:
        bg.close()
    return links


#{'Shorty "Вундеркинд"': 'f9688e62-42c5-9f10-f160-49abaee2e02c', 'Sheriff "Странник"': 'b9bf9657-411e-8fe3-b717-b99ba01fe07a', 'Frenzy "Демон"': '4add59eb-41f6-4184-3cb6-c89a81b6739b', 'Spectre "Винил"': '6803ed34-46cc-ba84-9e58-f78f6538151e', 'Онимару Куницуна': '901abab9-4a44-09f1-b892-9887a587f079', 'Sheriff "Конец игры"': '443f5a29-4d5e-d63e-a3c6-ada7713172fa', 'Stinger "Гроза оборотней"': '7ffbef55-4108-945e-6bc9-7b897f386d1b', 'Bulldog "Radiant Entertainment System"': '7deb8bd7-4ff6-64d2-1f23-2fb7143a5d98', 'Нож "Боец"': '21d49b4a-49ce-79f9-4e08-67959f8d17b5', 'Judge "Аквапринт"': '2a25f841-4769-6536-ded3-8890ee26c430', 'Bucky "Аквапринт"': '338bb3e6-4c47-425d-32a5-5ea1a96c78ae', 'Judge "Усмиритель"': '2d535295-4ad0-bcb1-1ab7-b8b0617a9abc', 'Frenzy "Коалиция: Кобра"': '337b4e6a-46d8-8359-50c0-388717617044', 'Bulldog "Демон"': '94456e3a-459f-4447-cc0d-7e9b5d01b81e', 'Vandal ".SYS"': 'e9953add-4069-d71b-447a-a8ad94fe6526', 'Ghost "Либретто"': '975b222c-430d-b59a-71b7-7cac1461b276', 'Bulldog "Боец"': '842dbe37-4bc7-95b3-26d7-a0af65615d5e', 'Shorty "Завиток"': '10cf91e9-4902-3898-3857-b4ad13882e71', 'Vandal "Нептун"': '49cea67c-4552-13c2-6b4b-8ba07761504e', 'Sheriff "Новый фронтир"': 'd9f04b7a-4ca6-1083-3af4-e3810bf15440', 'Stinger "Схема"': '0329743b-4ce8-be9f-b531-f4aadc890287', 'Stinger "Конструктор"': 'd9b038d8-4f8c-e4a6-e538-6e9cfb0dbb11', 'Веер "Пламя"': '445de3d7-4833-5bf7-ef75-aeb4a0212229', 'Phantom "Скорость"': '4707bae8-4938-71b5-ce5c-52aad3f24d21', 'Bulldog "Перелив"': '49b2e3c2-447c-7aba-ca50-a8993a72d969', 'Bulldog "Винил"': '9db51105-45a7-d05e-6d7d-08962c65c386', 'Stinger "Либретто"': 'bf4bee28-45f5-a512-5ccc-3284ad7ba59a', 'Classic "Усмиритель"': '60f3166c-4a22-9d8c-519a-f09b5fa1416b', 'Vandal "Город монстров"': 'eaf52d49-4608-45d9-5f18-c8b12614e01f', 'Phantom "Конструктор"': '0d203d6e-4944-7341-5f43-46a563b084c5', 'Vandal "Демон"': '9246f649-40b1-4077-31d1-be856acf5dd9', 'Frenzy "Под напряжением"': '08e6ba32-4a6e-8680-df58-39af9c32cdac', 'Frenzy "РагнаРокер"': 'b02520dd-48cd-466c-977d-529dc6a1d6f5', 'Sheriff "Империум"': 'e63cee8f-47b4-1d3d-6eb2-5b9a59f1aa2a', 'Frenzy "Фуксия"': '7b04cfc0-4c93-3bcb-7f3a-e189611412e3', 'Frenzy "Аквапринт"': 'c485b3df-4ea3-d457-e75b-35add7e78e7e', 'Marshal "Конструктор"': 'b878ea87-4383-caeb-ce4b-f7a37f42bb02', 'Odin "Коалиция: Кобра"': 'dd2acfca-4366-7ac0-c13e-1eb2f1948273', 'Ghost "Radiant Entertainment System"': 'b0c41f3b-4fa8-3768-4436-a29fbef94a68', 'Посох руи': 'dd587e30-4932-6cd4-3437-a1a043dd6a78', 'Bucky "Панорама"': '7f56c527-4185-be0e-a0ea-18b31a781c90', 'Guardian "Аквапринт"': '0ab465ed-4539-16f1-b791-5384280e0a1c', 'Classic "Мастерство"': '30f3e881-43d0-a455-b272-e8968c45761f', "Ares ''Небесная свинка''": '75e66837-47b4-0aec-cf8e-8b96f3af7d6b', 'Ghost "Гроза оборотней"': '04c6f57c-4463-f8b7-a475-6c89b2ec4416', 'Ghost "Звездная одиссея"': '0235ff00-4ba4-2092-ea7d-b99299d7017f', "Judge ''Небесная свинка''": '7ae57ece-4560-236b-5bdb-5f8ee2c294b2', 'Ares "Силуэт"': 'ba8b956f-4856-4946-9ae0-248201f1ed9e', 'Sheriff "Конструктор"': '77445d85-4b8a-3008-f98e-c3a42f72044a', 'Sheriff "Бессмертие"': 'd3f40fb9-40ec-b61f-7479-ceaded7b176a', 'Operator "Radiant Entertainment System"': '722a1311-43e1-7c18-ce90-acac33e9c2ad', 'Phantom "Чаропанк"': '82da0235-41c6-4a04-8296-e9baaa8f12a0', 'Кунай "Champions\xa02023"': '19c97db0-4ea8-d0de-d2a9-398eecb07298', 'Stinger ".SYS"': '50e072a5-4f30-63a9-6dee-a8b33781269f', 'Guardian "Лунная битва"': 'c04a92d3-445a-1d3c-07fb-99ba9637c0bd', "Marshal ''Небесная свинка''": '3711156a-43c5-de94-3ccc-ee8bae5e6df0', 'Bulldog "Усмиритель"': 'ae2bac38-48c3-a8b0-e843-eea29fab477b', 'Vandal "Стражи света"': '968efd06-4549-65f4-9fb1-3f90d612e428', 'Sheriff "Защитник"': 'd9fc55c6-4b92-98ac-5052-2a8b5ca4fb71', 'Vandal "Гроза оборотней"': 'f158e7d9-4404-1e88-747e-bf98da9a744b', 'Judge "Цифровая магия"': '64f5eaef-434b-69c5-5014-36a58ec1de20', 'Frenzy "Лунная битва"': '205449a6-45b6-e045-fe74-b09e9cc6d713', 'Vandal "Перелив"': '3c64689e-4bee-6e6e-8681-fdb9ee6b110f', 'Bulldog "Либретто"': 'bd7c039b-4ccc-1a20-acbf-dda25431e350', 'Bulldog "Цифровая магия"': 'c58376cc-41f8-ba0b-c42d-319b135ab994', 'Vandal "Чаропанк"': 'a0801408-4a88-3bc7-df50-0baaecf5040b', 'Judge "Коалиция: Кобра"': 'fe644484-4d07-5472-9e4a-d3992f2f2ecb', 'Marshal "Лунная битва"': 'f92d4bee-43a0-76e0-b07a-e6a064749617', 'Нож "Перелив"': '45159daa-423b-200a-c043-babdec9d0fd8', 'Vandal "Ион"': 'a8c10620-46a8-794e-be55-a0a13edb8d44', 'Bulldog "Скорость"': '7561a8e0-4cc4-8644-a88b-48a88790b36f', 'Operator "Либретто"': 'd3b378f7-4276-a4b5-2ef4-45a580c0ced6', 'Operator "Фуксия"': '93f788fa-4fb5-b372-ce71-b6b413ce0902', 'Ghost "Мастер"': 'b70db444-4ede-9cee-25dd-35b2edb38cd5', 'Sheriff "Город монстров"': 'f3d205b2-4975-3688-6613-039648e3a226', 'Ghost "Фрихэнд"': '21f136ee-4fd6-22dd-56c9-a9869ef31dda', 'Frenzy "Бросок"': '2f911f78-46e4-102a-f677-37a069c3a4dc', 'Искра "Чаропанк"': '35792a19-4e62-f3bc-f5df-289599d6cafc', 'Frenzy "Полет"': '2f69bfe0-4126-4d2b-91b4-c9a2cb1909da', 'Classic "9\xa0жизней"': 'b2ae014f-4c4e-1308-d1c7-e8bc70c46947', 'Marshal "Фрихэнд"': '30240598-46fb-8f6d-4923-1c957f468718', 'Ares "Отважный герой"': '6ab209eb-4596-c1f5-0262-22ac9f2beaa0', 'Operator "Отважный герой"': 'a7ec8cbf-499b-31cc-d58f-a2a900d7239c', 'Равновесие': 'ef67d6cb-4f7f-28ce-2973-cf90a97ae54d', 'Operator "Боец"': '3cd5ed19-405b-9600-489f-4e84900ea2d3', 'Guardian "Панорама"': 'a8c576f3-4c82-f631-6d2d-9fb99f2053fa', 'Stinger "Лунная битва"': 'b50b4766-492d-56b0-0bc3-bea6eba2606d', 'Spectre "Боец"': '6c69c2bc-4c7a-6308-8384-a1b2aa00a50b', 'Ghost "Вендетта"': '4526a891-4754-da6c-7ada-95a8a259952e', 'Judge "Империум"': '4f44cdaa-4810-efd2-0531-5d9565a4ec39', 'Sheriff "Схема"': 'b5601f65-4467-7946-8a37-45bed5514f98', 'Operator "Империум"': '176e6fa8-472d-9eb1-a474-11a3080c4053', 'Холодное оружие ".SYS"': '9d9ec56d-4973-3531-64f5-6d8eb2beb0a2', 'Odin "Гроза оборотней"': 'e1a05cb4-4ac5-b15a-e86e-bab0f7e093ad', 'Sheriff ".SYS"': '6287a1f1-4d10-5190-86ec-659b26020e87', 'Marshal "Песчаная буря"': '3296826f-4973-d5e1-e360-548ba5598faf', 'Frenzy "Силуэт"': '7dee6b38-400a-c9a4-3bac-cb87876e2873', 'Classic "Боец"': '564806a9-43fd-986e-7901-6790b6077a0d', 'Spectre "Фрихэнд"': '607e86c7-4ddf-4fa7-4fdb-c5a6013a90f8', 'Vandal "Отважный герой"': 'c8931118-40b7-dfb6-c071-85be21d51b4d', 'Ghost "Цифровая магия"': '9e0cfab0-428d-8eba-c554-ebac2614e43f', 'Judge "Силуэт"': '89af4c8b-4649-d61a-e1c3-fe95a90bae6a', 'Bucky ".SYS"': 'b7652717-49c0-b658-529e-6f8146ab0eca', 'Ghost "Отважный герой"': '604fa485-43ba-0fcf-4bad-f9a4e3b6c652', 'Vandal "Champions\xa02023"': '69f94fda-4603-744a-87fe-2391be7462e8', 'Клинок "Империум"': '1d7449fe-4bba-e213-c0c2-39816ca1043f', 'Spectre "Скорость"': '5172ea04-432f-2bfb-2163-808ccc2442c3', 'Vandal "Прайм"': 'c9678d8c-4327-f397-b0ec-dca3c3d6fb15', 'Shorty "Скорость"': 'c6db7920-4d61-556e-7c06-19954b847cbe', 'Marshal "Коалиция: Кобра"': '4dd7d0b9-40a9-de6c-ac61-aea19a6d8a77', "Frenzy ''Небесная свинка''": 'e44b70cf-4e83-19d3-a748-5f849054dad7', 'Odin "Фрихэнд"': '7d9adf46-48c5-9247-7121-1ba9e328e70c', 'Shorty "Змеиный укус"': '6f90d1ed-4acc-d925-4a8a-60913f14d16b', 'Керамбит "Скорость"': 'c01062ab-48ed-11a2-46bb-dba096daca59', 'Shorty "Винил"': '31629ef7-47ac-908e-369b-16beabc02c5b', 'Classic "Последняя надежда"': 'bbbe4b32-457c-e4fb-a674-1d9c3885d331', 'Power Fist': 'f2090053-4392-37bf-18bc-e7a03c1ebd82', 'Phantom "Прайм//2.0"': '9dc0bdd7-4d88-9360-38d6-3ea62b1daaca', 'Phantom "Radiant Entertainment System"': '28a7fd58-425c-6aa7-40d6-539d5fdac46c', 'Spectre "Песчаная буря"': '288073b8-4b6d-cef3-cbbe-49bb21670090', 'Phantom "Радиояд"': '21e0eb12-4211-3346-f01b-7b82c7931320', 'Усмиритель ': '76722e7d-4a64-a76e-98a7-0b9ec7d107e2', 'Shorty "Перелив"': '42a5b584-468b-0812-3041-7cb8b36cc0f8', 'Ghost "Тихарь"': 'afcb2528-4415-0178-98b1-c0a751092762', 'Vandal "Империум"': '43e7b969-4d2b-6d7b-6430-81bb37767481', 'Odin "Схема"': '15a5516d-412f-2db0-6bb3-3cbe40a2355f', 'Ares "Демон"': '8b829b66-44ad-c5d3-4e03-f5bc3c6f5d12', 'Ares "Город монстров"': 'de269cd5-448a-7374-db37-ad8e54a4d70d', 'Vandal "Араксис"': 'a3dba920-44ee-d7c5-5227-99a80aee3bd9', 'Vandal "Жнец"': 'ba42fe63-457a-78ce-4499-47950a698129', 'Spectre "Фуксия"': 'f3e9786c-44f4-712e-8033-c99c90d55e1b', 'Classic "Панорама"': 'd8bf97ac-4bc6-4896-1ca0-48b6545a64ab', 'Guardian "Фуксия"': '80fd2b3e-4854-204b-718d-aeaaeb5b63a5', 'Vandal "Схема"': '76c30002-4884-8193-dcf6-93a00b10bc15', 'Ares "Цифровая магия"': 'cba40da2-40b5-7f53-14f8-60a82bcdeee8', 'Ghost "Жнец"': 'a6fe7710-4edc-5e23-223d-aeaef3d17866', 'Stinger "Перелив"': '066522e1-4d71-d514-2943-70a1df85badf', 'Нож "Конструктор"': '54aa7ea7-4839-65b3-e0a8-d6a6aeb945fd', 'Phantom "Усмиритель"': 'efd31e00-4a50-2b1d-e27f-dfa5bc9687f2', 'Нож "VALORANT GO! Вып. 1"': '6e37a33a-416e-fcc0-ceb8-7784e18fbfe9', 'Spectre "Город монстров"': '700e2ea1-474a-c575-1957-88a038e61982', 'Ghost "Монарх"': 'ed8a1109-4e48-f077-636b-e98dd332bfcc', 'Vandal "Предвестник хаоса"': '1010fb40-4344-6ec8-2a8a-33bf076339b6', 'Ghost "Головоломка"': 'd0793c86-471d-c60c-b0da-bcbadcd8bf12'}

def make_collection(name):
    collections = set()
    with open('../skins_info/collection_data.json', 'r', encoding='UTF8') as file:
        collection_data = json.load(file)
        found = False  # Используем флаг для отслеживания наличия элемента в списке
        for collection, list_skins in collection_data.items():
            if name in list_skins:
                print(f'Element "{name}" found in {collection}')
                found = True
                collections.add(collection)
        if not found:
            print(f'Element "{name}" not found in any collection')
            return None
    return collections

image_skins('RU')
