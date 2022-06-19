import requests
from pprint import pprint

with open('VKtoken.txt') as vk:
    vk_token = vk.readline().strip()


class VK:
    def __init__(self, vk_id):
        self.vk_query = 'https://api.vk.com/method'
        self.params = {
            'access_token': vk_token,
            'v': 5.131
        }
        self.vk_id = self._get_id(vk_id)

    def _get_id(self, user_id: str):
        get_id_param = {'user_ids': user_id}
        query = f'{self.vk_query}/users.get'
        user_id = requests.get(query, params=self.params | get_id_param).json()['response'][0]['id']
        return user_id

    def get_albums(self):
        get_albums_params = {'owner_id': self.vk_id, 'need_system': 1}
        query = f'{self.vk_query}/photos.getAlbums'
        albums_items = requests.get(query, params=self.params | get_albums_params).json()['response']['items']
        albums_id = {albums_items[i]['title']: albums_items[i]['id'] for i in range(len(albums_items))}
        return albums_id

    def get_photo(self, album_id, count_photo):

        get_photo_params = {
            'owner_id': self.vk_id,
            'album_id': str(album_id),
            'rev': 1,
            'extended': 1,
            'photo_size': 1,
        }

        query = f'{self.vk_query}/photos.get'
        items = requests.get(query, params=self.params | get_photo_params).json()['response']
        return items

