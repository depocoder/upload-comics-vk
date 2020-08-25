import os
import requests
from dotenv import load_dotenv


def download_comic(id_comic):
    url = f'https://xkcd.com/{id_comic}/info.0.json'
    response = requests.get(url)
    decoded_response = response.json()
    url_comic = decoded_response['img']
    download_response = requests.get(url_comic)
    filename = f'comic{id_comic}.jpg'
    with open(filename, 'wb') as file:
        file.write(download_response.content)
    return decoded_response['safe_title']


def get_upload_url(group_id, vk_token):
    url_get = ('https://api.vk.com/method/photos.getWallUploadServer?')
    response = requests.get(url_get, params={
        "group_id": group_id,
        "access_token": vk_token,
        'v': '5.122'
    })
    return response.json()['response']['upload_url']


def upload_photo_on_server(group_id, vk_token, upload_url):
    with open("comic614.jpg", 'rb') as file:
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
    name_comic = download_comic(614)
    upload_url = get_upload_url(group_id, vk_token)
    server, photo, hash = upload_photo_on_server(group_id, vk_token, upload_url)
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
    print(owner_id)
    url_get = f'https://api.vk.com/method/wall.post?'
    response = requests.post(url_get, params={
        "attachments": f"photo{owner_id}_{id_pic}",
        "access_token": vk_token,
        'v': '5.122'

    })
    print(response.text)