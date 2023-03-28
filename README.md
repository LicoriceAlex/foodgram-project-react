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
asgiref==3.6.0
certifi==2022.12.7
cffi==1.15.1
charset-normalizer==3.1.0
coreapi==2.3.3
coreschema==0.0.4
cryptography==39.0.2
defusedxml==0.7.1
Django==3.2.10
django-cors-headers==3.14.0
django-filter==22.1
django-templated-mail==1.1.1
djangorestframework==3.14.0
djoser==2.1.0
flake8==5.0.4
flake8-broken-line==0.6.0
flake8-isort==6.0.0
flake8-plugin-utils==1.3.2
flake8-return==1.2.0
idna==3.4
isort==5.8.0
itypes==1.2.0
Jinja2==3.1.2
MarkupSafe==2.1.2
mccabe==0.7.0
oauthlib==3.2.2
pep8-naming==0.13.3
Pillow==9.4.0
psycopg2-binary==2.9.5
pycodestyle==2.9.0
pycparser==2.21
pyflakes==2.5.0
python-dotenv==0.19.0
python3-openid==3.2.0
pytz==2022.7.1
requests==2.28.2
requests-oauthlib==1.3.1
six==1.16.0
social-auth-app-django==4.0.0
social-auth-core==4.3.0
sqlparse==0.4.3
tomli==2.0.1
uritemplate==4.1.1
urllib3==1.26.15
gunicorn==20.1.0
Docker==23.0.1
Docker-compose==1.29.2
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
