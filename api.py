import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON с уникальным
        ключем пользователя"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = ""):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo):
        """Метод постит на сервер данные о новом питомце и возвращает статус запроса на сервер и результат в формате
        JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url+f'api/pets/{pet_id}', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except requests.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + f'api/pets/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except requests.JSONDecodeError:
            result = res.text
        return status, result

    def add_pet_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод добавляет фото питомца"""
        data = MultipartEncoder(
            fields={'pet_photo':(pet_photo, open(pet_photo, 'rb'), 'image/jpeg')})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+f'api/pets/set_photo/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
            result['pet_photo'] = pet_photo
        except requests.JSONDecodeError:
            result = res.text
        return status, result


    def get_api_key_invalid(self, email: str, password: str) -> json:
        """Метод делает невалидный запрос к API сервера"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except requests.JSONDecodeError:
            result = res.text
        return status, result