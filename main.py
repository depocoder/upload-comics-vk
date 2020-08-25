import os
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
        response_upload = requests.post(upload_url, files=files)
        response_upload.raise_for_status()
    decoded_response_upload = response_upload.json()
    server = decoded_response_upload['server']
    photo = decoded_response_upload['photo']
    hash = decoded_response_upload['hash']
    return server, photo, hash


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    group_id = os.getenv('GROUP_ID')
    comic_id = 615
    comic_name = get_comic_info(comic_id)['safe_title']
    upload_url = get_upload_url(group_id, vk_token)
    server, photo, hash = upload_photo_on_server(group_id, vk_token, upload_url, comic_id)
    url_get = f'https://api.vk.com/method/photos.saveWallPhoto?'
    response_uploadd = requests.post(url_get, params={
        "server": server,
        'photo': photo,
        'hash': hash,
        "group_id": group_id,
        "access_token": vk_token,
        'v': '5.122'
    })
    id_pic = response_uploadd.json()['response'][0]['id']
    owner_id = response_uploadd.json()['response'][0]['owner_id']
    url_get = f'https://api.vk.com/method/wall.post?'
    response = requests.post(url_get, params={
        "attachments": f"photo{owner_id}_{id_pic}",
        'owner_id': f'-{group_id}',
        "message": comic_name,
        "access_token": vk_token,
        'v': '5.122'

    })