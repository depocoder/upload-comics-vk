import os
import requests
from dotenv import load_dotenv


def gowload_comic(id_comic):
    url = f'https://xkcd.com/{id_comic}/info.0.json'
    response = requests.get(url)
    decoded_response = response.json()
    url_comic = decoded_response['img']
    response = requests.get(url_comic)
    filename = f'comic{id_comic}.jpg'
    with open(filename, 'wb') as file:
        return file.write(response.content)


def upload_photo_on_server(group_id, access_token):
    url_get = ('https://api.vk.com/method/photos.getWallUploadServer?' +
        f'group_id={group_id}&access_token={access_token}&v=5.122')
    response = requests.get(url_get)
    with open("comic614.jpg", 'rb') as file:
        upload_url = response.json()['response']['upload_url']
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
    chat_id = os.getenv('CHAT_ID')
    access_token = os.getenv('ACCESS_TOKEN')
    group_id = os.getenv('GROUP_ID')
    gowload_comic(id_comic)
    server, photo, hash = get_url_upload(group_id, access_token)
    url_get = f'https://api.vk.com/method/photos.saveWallPhoto?group_id=198114184&access_token={access_token}&v=5.122'
    response_uploadd = requests.post(url_get, params={
        "server": server,
        'photo': photo,
        'hash': hash
    })
    print(response_uploadd.json())
