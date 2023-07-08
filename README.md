# Foodgram_project 
### Описание:

Foodgram это сайт где пользователи могут публикавать вкусные рецепты.

### Авторизованный пользователь может:
   - Входить в систему под своим логином и паролем.
   - Выходить из системы (разлогиниваться).
   - Менять свой пароль.
   - Создавать/редактировать/удалять собственные рецепты
   - Просматривать рецепты на главной.
   - Просматривать страницы пользователей.
   - Просматривать отдельные страницы рецептов.
   - Фильтровать рецепты по тегам.
   - Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
   - Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингредиентов для рецептов из списка покупок.
   - Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.
### Неавторизованный пользователь может:
   - Создать аккаунт.
   - Просматривать рецепты на главной.
   - Просматривать отдельные страницы рецептов.
   - Просматривать страницы пользователей.
   - Фильтровать рецепты по тегам.
### Администратор может:
Администратор обладает всеми правами авторизованного пользователя. 
Плюс к этому он может:

   - изменять пароль любого пользователя,
   - создавать/блокировать/удалять аккаунты пользователей,
   - редактировать/удалять любые рецепты,
   - добавлять/удалять/редактировать ингредиенты.
   - добавлять/удалять/редактировать теги.
### Технологии:

- Python 3.11.2
- Docker
- Nginx
- Django 4.2.3
- djangorestframework 3.14.0

- postgres:13.0-alpine


### Запуск проекта:

* Установите Windows Subsystem for Linux по [инструкции с официального сайта Microsoft](https://learn.microsoft.com/ru-ru/windows/wsl/install). 
* скачайте и запустите [установочный файл Docker Desktop](https://www.docker.com/products/docker-desktop/).
* После установки запустите Docker Desktop
* Docker Desktop готов к работе! Зелёная полоска с китом в левом нижнем углу окна приложения означает, что докер-демон успешно запустился.
* Клонируйте репозиторий и перейдите в него в командной строке:
```
mkdir foodgram
```
```
cd foodgram
```
```
git clone https://github.com/KomkovAleksey/foodgram-project-react
```
* Создайте .env файл в корневой папке проекта.
В файле должны быть указаны: 
```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
DB_HOST=
DB_PORT=
SECRET_KEY=
ALLOWED_HOSTS=
```
### Запуск проекта в dev-режиме
* Поднимаем сеть контейнеров
```
cd infra
docker compose up
```
* В отдельном окне терминала выполните миграции, соберите статику  бэкенда и скопируйте её в /backend_static/static/:
```
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```
* Проект доступен по адоесу:
```
http://localhost:80/
```
### Запуск проекта на удаленном сервере:
* Откройте терминал и подключитесь к вашему  удалённому серверу:
```
ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом_без_расширения login@ip
```
* Установите Docker на сервер:
```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin
```
* Создайте папку kittygram
```
mkdir foodgram
```
* Скопируйте в папку файл docker-compose.production.yml:
```
scp ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом_без_расширения docker-compose.production.yml login@ip:kittygram/docker-compose.production.yml
```
* Скопируйте в папку ваш .env файл:
```
scp ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом_без_расширения .env login@ip:kittygram/.env
```
* или создайте его на сервере:
```
cd foodgram

sudo touch .env
```
```
Не забудьте заполнить .env:
sudo nano .env
```
* Переходите в папку foodgram/ и запустите docker compose в режиме демона:
```
sudo docker compose -f docker-compose.production.yml up -d
```
* Выполните миграции, соберите статику  бэкенда и скопируйте её в /backend_static/static/:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```
* Откройте конфиг Nginx:
```
sudo nano /etc/nginx/sites-enabled/default
```
* Измените location:
```
Было так:

# До этой строки — остальная часть секции server
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
    }

    location / {
        root   /var/www/kittygram;
        index  index.html index.htm;
        try_files $uri /index.html =404;
    }
# Ниже идёт часть про certbot 
```
```
Должно стать так:

# Всё до этой строки оставляем как было.
    location / {
        proxy_set_header Host $http_host;
        proxy_pass http://127.0.0.1:80;
    }
# Ниже ничего менять не нужно. 
```
* Проверьте работоспособность конфига и перезапустите Nginx:
```
sudo nginx -t 
sudo service nginx reload
```
* Проект доступен по адоесу:
```
http://localhost:80/
```
## Примеры запросов к API
Все запросы делались в приложении [Postman](https://www.postman.com/)

Создание пользователя:


### Автор
Алексей Комков
