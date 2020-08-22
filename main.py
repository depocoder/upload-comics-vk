import requests
from dotenv import load_dotenv


chat_id = os.getenv('CHAT_ID')
id_comic = 614
url = f'https://xkcd.com/{id_comic}/info.0.json'
response = requests.get(url)
decoded_response = response.json()
url_comic = decoded_response['img']
print(decoded_response['alt'])
response = requests.get(url_comic)
filename = f'comic{id_comic}.jpg'
with open(filename, 'wb') as file:
    file.write(response.content)
