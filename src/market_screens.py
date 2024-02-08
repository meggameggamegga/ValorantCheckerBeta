# Определите путь к папке с изображениями
import json
import os
import logging
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger('app.base')
def image_skins_market(lang,skin_full=None):

    skin_full = dict(sorted(skin_full.items()))
    links = []
    images_folder = r'src\photos\photo'
    # Определите размер фонового изображения
    background_width = 1260
    background_height = 200
    # Определите путь к папке, в которой нужно сохранить созданные фоны
    output_folder = r'accept_photo'
    # Создайте пустой фон
    #background = Image.open(r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\market.jpg')#Image.open(r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\night_market.jpg')
    background = Image.new('RGBA', (background_width, background_height), (39, 39, 39))  # 0,0,0,255
    # Создайте объект ImageDraw для добавления текста
    draw = ImageDraw.Draw(background)
    # Задайте шрифт и размер текста
    font = ImageFont.truetype("ariblk.ttf", 20)
    # Задайте текст и его позицию
    text = "@checker_valo_bot"
    text_position = (550, background_height -35)
    # Нарисуйте текст на изображении
    draw.text(text_position, text, fill=(255, 255, 255, 255), font=font)
    # Определите отступы для вставки изображения
    #if len(skin_full)>100:
    x_offset = 15
    y_offset = 7
    #else:
        #x_offset = 40
        #y_offset = 20
    # Максимальное количество изображений на одном фоне
    #if len(skin_full) > 100:
    max_images_per_background = 40
    #else:
    #    max_images_per_background = 21
    current_image_count = 0
    # Список для хранения всех созданных фонов
    backgrounds = []
    # Пройдитесь по данным и вставьте изображения на фон
    for k, url in skin_full.items():
        url_link = url[0]
        price = url[1]
        name = k
        try:
            if url[0]:
                # Полный путь к файлу
                image_path = os.path.join(images_folder, f'{url_link}.jpg')#
                # Проверка наличия файла
                if os.path.exists(image_path):
                    #if len(skin_full)>100:
                    image = Image.open(image_path).resize((200, 70))  # Скин картиинка
                    #else:
                    #    image = Image.open(image_path).resize((120, 70))
                    #Тут цвет фона
                    background_color = make_color(name=name,lang=lang)

                    #if len(skin_full) > 100:
                    image_with_background = Image.new('RGB',(300,147),(background_color))
                    #image_with_background = Image.open(background_color).resize((150,70))
                    image_with_background.paste(image, (35, 45), image)  # Это вставка и коорди
                    # Пишем имя скина
                    draw_name_skin = ImageDraw.Draw(image_with_background)
                    draw_price_skin = ImageDraw.Draw(image_with_background)
                    #if len(skin_full) > 100:

                    font_name = ImageFont.truetype("ariblk.ttf", 15)
                    text_color = (255, 255, 255, 255)  # Цвет текста (черный)
                    draw_price_skin.text((225,5),price,fill=text_color,font=font_name)
                    draw_name_skin.text((10, 120), name, fill=text_color, font=font_name)
                    # Вставьте изображение на фон с указанными отступами
                    background.paste(image_with_background, (x_offset, y_offset))
                    # Обновите отступы для следующего изображения
                    x_offset += image_with_background.width + 10
                    current_image_count += 1
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



def make_color(name,lang):
    color_tiers = {'EXCLUSIVE':(80,61,49), #r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\EXCLUSIVE.png', #Темно оранджевый
                   'PREMIUM':(73,48,59), #'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\PREMIUM.png',#Темно фиолетовый
                   'DELUXE':(31,61,58), #r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\DELUXE.png',#Зеленый
                   'ULTRA':(81,74,51),#r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\ULTRA.png',#Светло желтый
                   'SELECT':(31,61,58),#r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\DELUXE.png',#Голубой
                   'BATTLEPASS':(31,61,58),#r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\DELUXE.png'
                   }
    if lang == 'RU':
        with open(r'skins_info\collections_tier.json', 'r', encoding='UTF8') as file:
            collection_data = json.load(file)

    else:
        with open(r'skins_info\collections_tier_eng.json', 'r') as file:
            collection_data = json.load(file)
    found = False  # Используем флаг для отслеживания наличия элемента в списке
    for collection, list_skins in collection_data.items():
        if name in list_skins:
            #print(f'Element "{name}" found in {collection}')
            found = True
            colot_tier = color_tiers[collection]
            return colot_tier
    if not found:
        #print(f'Element "{name}" not found in any collection')
        return (31,61,58)


#image_skins_market(lang='RU')