import requests


id_comic = 614
url = f'https://xkcd.com/{id_comic}/info.0.json'
response = requests.get(url)
url_comic = (response.json())['img']
response = requests.get(url_comic)
filename = f'comic{id_comic}.jpg'
with open(filename, 'wb') as file:
    file.write(response.content)
