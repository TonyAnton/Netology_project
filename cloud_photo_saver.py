import json
from pprint import pprint
from datetime import datetime
from vk_save import VK
from yandex import DownloadToYandex

vk_id_input = input('Введите id или короткое имя пользователя: ')
vk_user = VK(vk_id_input)
pprint(vk_user.get_albums())
while True:
    vk_album_id = int(input('Введите id альбома из списка выше: '))
    if vk_album_id in vk_user.get_albums().values():
        break
    else:
        print('Введен некорректный id альбома!')

count_photo_in_album = vk_user.get_photo(vk_album_id, count_photo=5)["count"]
pprint(count_photo_in_album)
while True:
    count_choose = input(f'Хотите выбрать количество фото для выгрузки (по умолчанию 5) и не более '
                         f'{count_photo_in_album}? да/нет: ').lower()
    if count_choose == 'да':
        while True:
            count_photo = input('Введите количество: ')
            if int(count_photo) <= count_photo_in_album:
                break
            else:
                print('Превышено количество фото или неверный ввод!')
        break
    elif count_choose == 'нет':
        count_photo = 5
        break
    else:
        print('Исправьте ответ!')

photo_user_dict = vk_user.get_photo(vk_album_id, count_photo)['items']

likes_url_dict = {}
json_list = []
like_list = []

for photo in photo_user_dict[:int(count_photo)]:
    likes = photo['likes']['count']
    date = datetime.utcfromtimestamp(photo['date']).strftime('%Y-%m-%d-%HH-%MM-%SS')
    size = photo['sizes'][-1]['type']
    photo_url = photo['sizes'][-1]['url']
    if f'{likes}.jpg' not in like_list:
        likes_url_dict[f'{likes}.jpg'] = photo_url
        json_list.append({'file_name': f'{likes}.jpg', 'size': size})
        like_list.append(f'{likes}.jpg')
    else:
        likes_url_dict[f'{likes} {date}.jpg'] = photo_url
        json_list.append({'file_name': f'{likes} {date}.jpg', 'size': size})

with open('photo_data.json', 'w') as datafile:
    json.dump(json_list, datafile, indent=4)

yandex_token = input('Введите токен для доступа к Яндекс.Диску: ')
yandex_user = DownloadToYandex(yandex_token)
yandex_user.upload_photo(likes_url_dict)
