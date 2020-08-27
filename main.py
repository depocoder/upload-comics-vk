import os
import sys
from random import randint
import requests
from dotenv import load_dotenv


def get_comic_info(comic_id):
    url = f'https://xkcd.com/{comic_id}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_comic(comic_id, url_comic):
    download_response = requests.get(url_comic)
    download_response.raise_for_status()
    filename = f'comic{comic_id}.jpg'
    with open(filename, 'wb') as file:
        return file.write(download_response.content)


def get_upload_url(group_id, vk_token):
    url_get = ('https://api.vk.com/method/photos.getWallUploadServer?')
    response = requests.get(url_get, params={
        "group_id": group_id,
        "access_token": vk_token,
        'v': '5.122'
    })
    return response.json()


def upload_photo_on_server(group_id, vk_token, upload_url, comic_id):
    with open(f"comic{comic_id}.jpg", 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
    decoded_response = response.json()
    server = decoded_response['server']
    photo = decoded_response['photo']
    upload_hash = decoded_response['hash']
    return server, photo, upload_hash


def save_wall_photo(group_id, vk_token, comic_id, upload_url):
    server, photo, upload_hash = upload_photo_on_server(
        group_id, vk_token, upload_url, comic_id)
    url = 'https://api.vk.com/method/photos.saveWallPhoto?'
    response = requests.post(url, params={
        "server": server,
        'photo': photo,
        'hash': upload_hash,
        "group_id": group_id,
        "access_token": vk_token,
        'v': '5.122'
    })
    return response.json()


def post_wall(id_pic, owner_id, comic_name, vk_token, group_id):
    url_get = 'https://api.vk.com/method/wall.post?'
    response = requests.post(url_get, params={
        "attachments": f"photo{owner_id}_{id_pic}",
        'owner_id': f'-{group_id}',
        "message": comic_name,
        "access_token": vk_token,
        'v': '5.122'
    })
    return response.json()


def delete_comic(random_comic_id):
    if os.path.exists(f'comic{random_comic_id}.jpg'):
        path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            f'comic{random_comic_id}.jpg')
        os.remove(path)


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    group_id = os.getenv('GROUP_ID')
    try:
        last_comic_id = get_comic_info('')['num']
        random_comic_id = randint(1, last_comic_id)
        comic_info = get_comic_info(random_comic_id)
        url_comic = comic_info['img']
        download_comic(random_comic_id, url_comic)
        comic_name = comic_info['safe_title']
    except requests.exceptions.HTTPError:
        sys.exit('Ошибка скачивания комикса.')
        delete_comic(random_comic_id)
    upload_info = get_upload_url(group_id, vk_token)
    if 'error' in upload_info:
        delete_comic(random_comic_id)
        sys.exit('Ошибка получения ссылки для загрузки, ' +
                 'проверьте подключение к интернету или ваш .env файл')
    upload_url = upload_info['response']['upload_url']
    decoded_response = save_wall_photo(
        group_id, vk_token, random_comic_id, upload_url)
    if 'error' in decoded_response:
        delete_comic(random_comic_id)
        sys.exit('Ошибка загрузки на сервер, ' +
                 'проверьте подключение к интернету или ваш .env файл')
    id_pic = decoded_response['response'][0]['id']
    owner_id = decoded_response['response'][0]['owner_id']
    post_wall_info = post_wall(id_pic, owner_id,
                               comic_name, vk_token, group_id)
    if 'error' in post_wall_info:
        delete_comic(random_comic_id)
        sys.exit('Ошибка публикации на сервер, ' +
                 'проверьте подключение к интернету или ваш .env файл')
    delete_comic(random_comic_id)
