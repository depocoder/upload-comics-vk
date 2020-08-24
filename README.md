# upload-comics-vk
 
## Описание проекта.   
Этот проект позволяет загружать комиксы с [сайта](https://xkcd.com/)
   
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
Ваше ID приложения в переменную **CHAT_ID** его можно получить [**тут**](https://vk.com/dev).  

    
**Пример заполнения .env файла**        
```
example=fjsdhgshl
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
