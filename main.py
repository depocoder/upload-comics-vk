import os
import requests
from dotenv import load_dotenv


chat_id = os.getenv('CHAT_ID')
access_token = os.getenv('ACCESS_TOKEN')
id_comic = 614
url = f'https://xkcd.com/{id_comic}/info.0.json'
response = requests.get(url)
decoded_response = response.json()
url_comic = decoded_response['img']
response = requests.get(url_comic)
filename = f'comic{id_comic}.jpg'
with open(filename, 'wb') as file:
    file.write(response.content)
url_get = f'https://api.vk.com/method/groups.get?access_token={access_token}&v=5.122'
response = requests.get(url_get)
print(response.text)
