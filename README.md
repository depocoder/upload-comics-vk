# upload-comics-vk
 
## Описание проекта.   
Этот проект позволяет загружать комиксы с [сайта](https://xkcd.com/) на стену вашей группы ВК.
   
## Пример использования.   

![](example.gif) 
## Подготовка к запуску.  (Linux or MacOS)
Уставновить Python 3+.
```
sudo apt-get install python3
```
Установить, создать и активировать виртуальное окружение.
```
pip3 install virtualenv
python3 -m venv env
source env/bin/activate
```
Установить библиотеки командой.  
```
pip3 install -r requirements.txt
```
Создайте файл .env в него надо прописать    
Ваш token приложения, чтобы его получить нужно создать приложение  [**тут**](https://vk.com/dev) ID приложения в переменную **client_id** ссылка ниже.    
```
https://oauth.vk.com/authorize?client_id=&scope=stories,photos,docs,manage,wall&response_type=token&v=5.122
```
Разрешаете доступ приложения к странице, копируете из адресной строки access_token и вставляете в переменную **VK_TOKEN**.
В переменную **GROUP_ID** пропишите id вашей группы, узнать group_id для вашей группы можно [**здесь**](http://regvk.com/id/)   
**Пример заполнения .env файла**        
```
VK_TOKEN=f26e2dca0a2f77894e6e292289i48c88d4339f084b302457a562a3b11d3ec56b01bd15da9001c5331bf13
GROUP_ID=195114184
```

# Аргументы.
**example** — etc..

```
python3 main.py ..
```
## Запуск кода.  
```
python3 main.py
```
