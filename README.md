выполнять из каталога ./mysite/

do: pip install djangorestframework
do: python manage.py makemigrations
do: python manage.py migrate
do: python manage.py runserver - запустить сервер из директории ./mysite/


python manage.py createsuperuser - создать админа

https://django.fun/docs/django/ru/3.2/intro/tutorial02/ - подключение базы данных (авто sqlite, настройка в settings.py)
C:\Program Files\Python38\lib\site-packages\django\db\backends\sqlite3\base.py - куда пушит бд

https://django.fun/docs/django/ru/3.2/intro/tutorial03/ - про странички в templates (html seems like jinja2)

### Полезные ссылки
https://djbook.ru/rel3.0/ref/request-response.html - Объекты ответа и запроса
https://django.fun/docs/django/ru/3.2/topics/db/queries/ - че по моделям данных


REST SERVER:
http://127.0.0.1:8000/
http://127.0.0.1:8000/student/

### Авторизация
TOKEN Авторизация:
  Создать пользователя
  
  Запрос токена:
    curl -X POST "http://localhost:8000/api-token-auth/" -d "username=$USERNAME;password=$PASSWORD"
    Будет получен токен для пользователя: {"token":"dfc5e301b7ea4c29523a15cacaf26ce7a48a00b8","user_id":1}
  Запросы:
    curl -X GET "http://localhost:8000/courses/" -H "Authorization: Token 021c5b815f3ad358deb93eb8ba03af9a281ffb33"
  

### EMAIL notifications
Настроить параметры:
EMAIL_BACKEND,
DEFAULT_FROM_EMAIL,
EMAIL_HOST,
EMAIL_PORT,
EMAIL_HOST_USER,
EMAIL_HOST_PASSWORD,
EMAIL_USE_TLS,
EMAIL_USE_SSL

отправить POST request на url: notify/mails/ 
с телом запроса:
```
{
    "subject": "Тема письма",
    "body": "Сообщение",
    "to": ["email@example.com", "to@example.com"]
}
```
