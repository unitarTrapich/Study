# Лабораторная работа №4
### Django Polls — Polls from the Crypt


Учебное Django-приложение для проведения опросов с регистрацией пользователей и подтверждением email  
(письма выводятся в консоль).

---

## Возможности
- Регистрация и авторизация пользователей
- Email-верификация аккаунта
- Голосование в опросах и просмотр результатов
- Разграничение прав (user / staff / admin)
- Админ-панель Django

---

## Быстрый старт
```bash
python -m venv .venv
source .venv/bin/activate
pip install django django-crispy-forms crispy-bootstrap5
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
````

Приложение доступно по адресу:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Email-подтверждение

* После регистрации письмо выводится в консоль
* Скопируйте ссылку активации и откройте в браузере
* До активации вход невозможен

---

## Основные URL

* `/polls/` — список опросов
* `/polls/<id>/` — голосование
* `/polls/<id>/results/` — результаты
* `/polls/register/` — регистрация
* `/polls/login/` — вход
* `/admin/` — админ-панель

---

## Тестирование

```bash
python manage.py test polls
```

---

## Стек

* Python, Django
* SQLite
* Django Templates
* Crispy Forms + Bootstrap 5

