import os
from random import randint
import requests
from dotenv import load_dotenv


def get_comic_info(comic_id):
    url = f'https://xkcd.com/{comic_id}/info.0.json'
    response = requests.get(url)
    return response.json()


def download_comic(comic_id):
    url_comic = get_comic_info(comic_id)['img']
    download_response = requests.get(url_comic)
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
    return response.json()['response']['upload_url']


def upload_photo_on_server(group_id, vk_token, upload_url, comic_id):
    with open(f"comic{comic_id}.jpg", 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
    decoded_response = response.json()
    server = decoded_response['server']
    photo = decoded_response['photo']
    hash = decoded_response['hash']
    return server, photo, hash


def save_wall_photo(group_id, vk_token, comic_id, upload_url):
    server, photo, hash = upload_photo_on_server(
        group_id, vk_token, upload_url, comic_id)
    url = 'https://api.vk.com/method/photos.saveWallPhoto?'
    response = requests.post(url, params={
        "server": server,
        'photo': photo,
        'hash': hash,
        "group_id": group_id,
        "access_token": vk_token,
        'v': '5.122'
    })
    return response.json()


def post_wall(decoded_response, comic_name, vk_token, group_id):
    id_pic = decoded_response['response'][0]['id']
    owner_id = decoded_response['response'][0]['owner_id']
    url_get = 'https://api.vk.com/method/wall.post?'
    response = requests.post(url_get, params={
        "attachments": f"photo{owner_id}_{id_pic}",
        'owner_id': f'-{group_id}',
        "message": comic_name,
        "access_token": vk_token,
        'v': '5.122'
    })
    return response


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    group_id = os.getenv('GROUP_ID')
    upload_url = get_upload_url(group_id, vk_token)
    num_last_comic = get_comic_info('')['num']
    random_comic_id = randint(1, num_last_comic)
    download_comic(random_comic_id)
    comic_name = get_comic_info(random_comic_id)['safe_title']
    decoded_response = save_wall_photo(
        group_id, vk_token, random_comic_id, upload_url)
    post_wall(decoded_response, comic_name, vk_token, group_id)
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        f'comic{random_comic_id}.jpg')
    os.remove(path)
