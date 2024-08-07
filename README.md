![status badge](https://github.com/KomkovAleksey/foodgram-project-react/actions/workflows/main.yml/badge.svg)



# 🍕 [Foodgram_project](https://foodgrampromo.zapto.org/recipes)


## Оглавление:

- [Технологии](#технологии)
- [Описание проекта](#Описание-проекта)
- [Права пользователей](#Права-пользователей)
- [Установка и запуск проекта](#установка-и-запуск-проекта)
- [Примеры запросов к API](#Примеры-запросов-к-API)
- [Автор](#Автор)

## Технологии:

- Python 3.11.2
- Docker
- Nginx
- Django 3.2.16
- djangorestframework 3.12.4
- postgres:13.0-alpine

## Данные для доступа к админ зоне:
сайт [foodgrampromo.zapto.org](https://foodgrampromo.zapto.org/recipes)

username - admin

логин - admin@admin.com

пароль - Praktikum+123

## Описание проекта:

Foodgram(«Продуктовый помощник») это кулинарный сайт, где пользователи могут публиковать свои рецепты,
добавлять чужие рецепты в избранное и подписываться на публикации других авторов.

## Права пользователей:

### Авторизованный пользователь может:
  1. Доступна главная страница.
  2. Доступна страница другого пользователя.
  3. Доступна страница отдельного рецепта.
  4. Доступна страница «Мои подписки»:

      a. можно подписаться и отписаться на странице рецепта;

      b. можно подписаться и отписаться на странице автора;

      c. при подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки.
  5. Доступна страница «Избранное»:
      a. на странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда;
      b. на любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда.
  6. Доступна страница «Список покупок»:
      a. на странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда;
      b. на любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда;
      c. есть возможность выгрузить файл с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок»;
      d. ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента.
  7. Доступна страница «Создать рецепт»:
      a. есть возможность опубликовать свой рецепт;
      b. есть возможность отредактировать и сохранить изменения в своём рецепте;
      c. есть возможность удалить свой рецепт.
  8. Доступна возможность выйти из системы.
### Неавторизованный пользователь может:
  1. Доступна главная страница.

  2. Доступна страница отдельного рецепта.
  3. Доступна страница любого пользователя.
  4. Доступна и работает форма авторизации.
  5. Доступна и работает форма регистрации.
### Администратор может:
Администратор обладает всеми правами авторизованного пользователя. 
Плюс к этому он может:

   - изменять пароль любого пользователя,

   - создавать/блокировать/удалять аккаунты пользователей,
   - редактировать/удалять любые рецепты,
   - добавлять/удалять/редактировать ингредиенты.
   - добавлять/удалять/редактировать теги.

## Установка и запуск проекта

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
В нем должны быть указаны. 
```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
DB_HOST=
DB_PORT=
SECRET_KEY=
ALLOWED_HOSTS=
```
В корневой папке есть файл .env.example,
с примером того как надо заполнять .env файл.
### Запуск проекта в dev-режиме:
* Поднимаем сеть контейнеров
```
cd infra
docker compose up
```
* Проект доступен по адоесу:
```
http://localhost:80/
```
* Cпецификация API:
```
http://localhost/api/docs/
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
* Создайте папку Foodgram:
```
mkdir Foodgram
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
cd Foodgram

sudo touch .env
```
```
Не забудьте заполнить .env:
sudo nano .env
```
* Переходите в папку Foodgram/ и запустите docker compose в режиме демона:
```
sudo docker compose -f docker-compose.production.yml up -d
```
* Выполните миграции, соберите статику  бэкенда и скопируйте её в /backend_static/static/:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```
* Наполните базу данных:
```
docker compose exec backend python manage.py import_ingredients_data
docker compose exec backend python manage.py import_tags_data
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



## Автор

[Алексей Комков](https://github.com/KomkovAleksey)
