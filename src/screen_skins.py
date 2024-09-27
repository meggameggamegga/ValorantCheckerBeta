# Определите путь к папке с изображениями
import json
import os
import logging
from PIL import Image, ImageDraw, ImageFont

#logger = logging.getLogger('app.base')
#def image_skins(skin_full,lang):
#    logger.info('Запуск image_skins')
#    skin_full = dict(sorted(skin_full.items()))
#    links = []
#    images_folder = 'photo'
#    # Определите размер фонового изображения
#    background_width = 1000
#    background_height = 1500
#    # Определите путь к папке, в которой нужно сохранить созданные фоны
#    output_folder = f'accept_photo/'
#    # Создайте пустой фон
#    #background = Image.open(r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\пывыпавыпа (2).png').resize((1000,1500))
#    background = Image.new('RGBA', (background_width, background_height), (39, 39, 39))  # 0,0,0,255
#    # Создайте объект ImageDraw для добавления текста
#    draw = ImageDraw.Draw(background)
#    # Задайте шрифт и размер текста
#    font = ImageFont.truetype("arial.ttf", 55)
#    # Задайте текст и его позицию
#    text = "@checker_valo_bot"
#    text_position = (255, background_height - 100)
#    # Нарисуйте текст на изображении
#    draw.text(text_position, text, fill=(255, 255, 255, 255), font=font)
#    # Определите отступы для вставки изображения
#    #if len(skin_full)>=100:
#    x_offset = 50
#    y_offset = 25
#    #else:
#    #    x_offset = 105
#    #    y_offset = 15
#    # Максимальное количество изображений на одном фоне
#    #if len(skin_full) >= 100:
#    max_images_per_background = 40
#    #else:
#    #    max_images_per_background = 30
#    current_image_count = 0
#    # Список для хранения всех созданных фонов
#    backgrounds = []
#    # Пройдитесь по данным и вставьте изображения на фон
#    for k, url in skin_full.items():
#        if lang == 'EU':
#            try:
#                name = k.split(' ')[1]
#            except Exception as e:
#                pass
#        else:
#            name = k.split(' ')[0]  # Для EN
#        try:
#            if url:
#                # Полный путь к файлу
#                image_path = os.path.join(images_folder, f'{url}.jpg')#
#                # Проверка наличия файла
#                if os.path.exists(image_path):
#                    #if len(skin_full)>100:
#                    image = Image.open(image_path).resize((170, 80))  # Скин картиинка
#                    #else:
#                    #    image = Image.open(image_path).resize((190, 85))
#                    #Тут цвет фона
#                    background_color = make_color(name=k)
#                    #if len(skin_full) >= 100:
#                    #image_with_background = Image.new('RGB', (210, 120), background_color)
#                    image_with_background = Image.open(background_color).resize((210,120))
#                    print(image_with_background.format)
#                    image_with_background.paste(image, (18, 15), image)  # Это вставка и коорди
#                    #else:
#                    #    image_with_background = Image.new('RGB', (250, 120), background_color)
#                    #    image_with_background.paste(image, (35, 12), image) #Это вставка и коорди
#                    # Пишем имя скина
#                    draw_name_skin = ImageDraw.Draw(image_with_background)
#                    #if len(skin_full) >= 100:
#                    font_name = ImageFont.truetype("arial.ttf", 12)
#                    #else:
#                    #    font_name = ImageFont.truetype('arial.ttf',14)
#                    text_skin = k  # Название скина из переменной k
#                    #if len(skin_full) >=100:
#                    text_position_skin = (6, 102)  # Позиция текста (x, y) на изображении
#                    #else:
#                    #    text_position_skin = (40, 102)  # Позиция текста (x, y) на изображении
#                    text_color = (255, 255, 255, 255)  # Цвет текста (черный)
#                    draw_name_skin.text(text_position_skin, text_skin, fill=text_color, font=font_name)
#                    # Вставьте изображение на фон с указанными отступами
#                    background.paste(image_with_background, (x_offset, y_offset))
#                    # Обновите отступы для следующего изображения по X
#                    x_offset += image_with_background.width + 20
#                    current_image_count += 1
#                    # Если x_offset превышает ширину фона
#                    if x_offset + image_with_background.width > background_width:
#                        #if len(skin_full) >= 100:
#                        x_offset = 50
#                        y_offset += image_with_background.height + 10
#                        #else:
#                        #    x_offset = 105
#                        #    y_offset += image_with_background.height + 20 #Обновить отступы по Y
#                    if current_image_count >= max_images_per_background:
#                        #if len(skin_full) >= 100:
#                        x_offset = 50
#                        y_offset = 15
#                        #else:
#                        #    x_offset = 105
#                        #    y_offset = 15
#                        current_image_count = 0
#                        # Сохраните текущий фон в список backgrounds
#                        backgrounds.append(background.copy())
#                        # Создайте новый фон
#                        background = Image.new('RGBA', (background_width, background_height), (39, 39, 39))
#                        draw = ImageDraw.Draw(background)
#                        # Задайте шрифт и размер текста
#                        font = ImageFont.truetype("arial.ttf", 55)
#                        # Задайте текст и его позицию
#                        text = "@checker_valo_bot"
#                        text_position = (255, background_height - 95)
#                        # Нарисуйте текст на изображении
#                        draw.text(text_position, text, fill=(255, 255, 255, 255), font=font)
#        except Exception as e:
#            print(f"Ошибка при обработке изображения: {e}")
#
#    # Сохраните оставшийся текущий фон
#    backgrounds.append(background)
#    # Закройте фоны
#    for i, bg in enumerate(backgrounds):
#        # Создайте имя файла с уникальным именем (например, background_1.png, background_2.png и т. д.)
#        output_path = os.path.join(output_folder, f'background_{i + 1}.png')  # label
#        bg.save(output_path)
#        links.append(output_path)
#    # Закройте фоны
#    for bg in backgrounds:
#        bg.close()
#    return links
#
#
#
#def make_color(name):
#    color_tiers = {'EXCLUSIVE':r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\EXCLUSIVE.png', #Темно оранджевый
#                   'PREMIUM':r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\PREMIUM.png',#Темно фиолетовый
#                   'DELUXE':r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\31,61,58.png',#Зеленый
#                   'ULTRA':r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\ULTRA.png',#Светло желтый
#                   'SELECT':r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\DELUXE.png',#Голубой
#                   'BATTLEPASS':r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\DELUXE.png'
#                   }
#    with open('collections_tier.json','r',encoding='UTF8') as file:
#        collection_data = json.load(file)
#        found = False  # Используем флаг для отслеживания наличия элемента в списке
#        for collection, list_skins in collection_data.items():
#            if name in list_skins:
#                found = True
#                colot_tier = color_tiers[collection]
#                return colot_tier
#        if not found:
#            return r'C:\Users\роман\PycharmProjects\valorant_checker_test_v2\DELUXE.png'
#
#
#

# Определите путь к папке с изображениями
import json
import os
import logging
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger('app.base')
def image_skins(skin_full,lang):
    logger.info('Запуск image_skins')
    skin_full = dict(sorted(skin_full.items()))
    print(skin_full)
    links = []
    images_folder = r'src/photos/photo'
    # Определите размер фонового изображения
    background_width = 1000
    background_height = 1500
    # Определите путь к папке, в которой нужно сохранить созданные фоны
    output_folder = f'accept_photo/'
    # Создайем пустой фон
    background = Image.new('RGBA', (background_width, background_height), (39, 39, 39))  # 0,0,0,255
    # Создайте объект ImageDraw для добавления текста
    draw = ImageDraw.Draw(background)
    # Задайте шрифт и размер текста
    font = ImageFont.truetype("arial.ttf", 55)
    # Задайте текст и его позицию
    text = "@checker_valo_bot"
    text_position = (255, background_height - 100)
    # Нарисуйте текст на изображении
    draw.text(text_position, text, fill=(255, 255, 255, 255), font=font)
    # Определите отступы для вставки изображения
    #if len(skin_full)>=100:
    x_offset = 50
    y_offset = 25
    #else:
    #    x_offset = 105
    #    y_offset = 15
    # Максимальное количество изображений на одном фоне
    #if len(skin_full) >= 100:
    max_images_per_background = 40
    #else:
    #    max_images_per_background = 30
    current_image_count = 0
    # Список для хранения всех созданных фонов
    backgrounds = []
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
                    #if len(skin_full)>100:
                    image = Image.open(image_path).resize((170, 80))  # Скин картиинка
                    #else:
                    #    image = Image.open(image_path).resize((190, 85))
                    #Тут цвет фона
                    background_color = make_color(name=k)
                    #if len(skin_full) >= 100:
                    image_with_background = Image.new('RGB', (210, 120), background_color)
                    image_with_background.paste(image, (18, 15), image)  # Это вставка и коорди
                    #else:
                    #    image_with_background = Image.new('RGB', (250, 120), background_color)
                    #    image_with_background.paste(image, (35, 12), image) #Это вставка и коорди
                    # Пишем имя скина
                    draw_name_skin = ImageDraw.Draw(image_with_background)
                    #if len(skin_full) >= 100:
                    font_name = ImageFont.truetype("ariblk.ttf", 12)
                    #else:
                    #    font_name = ImageFont.truetype('arial.ttf',14)
                    text_skin = k  # Название скина из переменной k
                    #if len(skin_full) >=100:
                    text_position_skin = (6, 102)  # Позиция текста (x, y) на изображении
                    #else:
                    #    text_position_skin = (40, 102)  # Позиция текста (x, y) на изображении
                    text_color = (255, 255, 255, 255)  # Цвет текста (черный)
                    draw_name_skin.text(text_position_skin, text_skin, fill=text_color, font=font_name)
                    # Вставьте изображение на фон с указанными отступами
                    background.paste(image_with_background, (x_offset, y_offset))
                    # Обновите отступы для следующего изображения по X
                    x_offset += image_with_background.width + 20
                    current_image_count += 1
                    # Если x_offset превышает ширину фона
                    if x_offset + image_with_background.width > background_width:
                        #if len(skin_full) >= 100:
                        x_offset = 50
                        y_offset += image_with_background.height + 10
                        #else:
                        #    x_offset = 105
                        #    y_offset += image_with_background.height + 20 #Обновить отступы по Y
                    if current_image_count >= max_images_per_background:
                        #if len(skin_full) >= 100:
                        x_offset = 50
                        y_offset = 15
                        #else:
                        #    x_offset = 105
                        #    y_offset = 15
                        current_image_count = 0
                        # Сохраните текущий фон в список backgrounds
                        backgrounds.append(background.copy())
                        # Создайте новый фон
                        background = Image.new('RGBA', (background_width, background_height), (39, 39, 39))
                        draw = ImageDraw.Draw(background)
                        # Задайте шрифт и размер текста
                        font = ImageFont.truetype("arial.ttf", 55)
                        # Задайте текст и его позицию
                        text = "@checker_valo_bot"
                        text_position = (255, background_height - 95)
                        # Нарисуйте текст на изображении
                        draw.text(text_position, text, fill=(255, 255, 255, 255), font=font)
        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")

    # Сохраните оставшийся текущий фон
    backgrounds.append(background)
    # Закройте фоны
    for i, bg in enumerate(backgrounds):
        output_path = os.path.join(output_folder, f'background_{i + 1}.png')  # label
        bg.save(output_path)
        links.append(output_path)
    # Закройте фоны
    for bg in backgrounds:
        bg.close()
    return links



def make_color(name):
    color_tiers = {'EXCLUSIVE':(80,61,49), #Темно оранджевый
                   'PREMIUM':(73,48,59),#Темно фиолетовый
                   'DELUXE':(31,61,58),#Зеленый
                   'ULTRA':(81,74,51),#Светло желтый
                   'SELECT':(31,61,58),#Голубой
                   'BATTLEPASS':(31,61,58)
                   }
    with open('skins_info/collections_tier.json','r',encoding='UTF8') as file:
        collection_data = json.load(file)
        found = False  # Используем флаг для отслеживания наличия элемента в списке
        for collection, list_skins in collection_data.items():
            if name in list_skins:
                found = True
                colot_tier = color_tiers[collection]
                return colot_tier
        if not found:
            return (31,61,58)


