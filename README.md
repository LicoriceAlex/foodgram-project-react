# Продуктовый помощник Foodgram
### Админка
```
Логин admin
пароль 123
```
```
http://158.160.25.92/
```
### Описание
На сайте Foodgram пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
Процедура запуска проекта представлена ниже.
### Технологии
Django Rest Framework
PostgreSQL
Docker
Docker-compose
### Шаблон наполнения env-файла
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
POSTGRES_DB=foodgram_db # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 

SECRET_KEY = <secret_key> # секретный ключ Django
```
### Запуск проекта, развертка контейнеров
- Заполните env-файл
- Перейдите в директорию foodgram-project-react/infra/
- Выполните команду 
```
docker-compose up -d
```
- Далее примените миграции, создайте суперпользователя и "соберите статику",
по очереди выполнив следующие команды:
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
```
### Авторы
LicoriceAlex, Yandex.Practicum
### Workflow status
![foodgram_workflow](https://github.com/LicoriceAlex/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
