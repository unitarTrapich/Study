# Лабораторная работа №3 Django Tutorial

## 1. Создание проекта
- `django-admin startproject mysite`
- `python manage.py startapp polls`
- `python manage.py runserver`

Проект — это сайт,  
приложение — отдельная функциональность.

---

## 2. URL и views
- URL описываются в `urls.py`
- Логика обработки — в `views.py`
- `path()` связывает URL и view
- `include()` подключает URL приложения

---

## 3. Модели и база данных
- Модели описываются в `models.py`
- Каждая модель = таблица в БД
- Основные поля: `CharField`, `DateTimeField`, `IntegerField`, `ForeignKey`

Миграции:
- `python manage.py makemigrations`
- `python manage.py migrate`

---

## 4. Шаблоны
- HTML хранится в `templates/`
- Используются переменные `{{ }}` и теги `{% %}`
- `render(request, template, context)` — вывод HTML

---

## 5. Админка
- `python manage.py createsuperuser`
- Модели регистрируются в `admin.py`
- Можно настраивать отображение (поля, фильтры, поиск)

---

## 6. Generic Views
- `ListView` — список объектов
- `DetailView` — детали объекта
- Уменьшают количество кода

---

## 7. Тестирование
- Тесты пишутся в `tests.py`
- `python manage.py test`
- Проверяют модели и представления

---

## 8. Статические файлы
- CSS, изображения → `static/`
- Подключение через `{% static %}`

---

## Основные команды
- `runserver` — запуск сервера
- `makemigrations`, `migrate` — БД
- `createsuperuser` — админ
- `test` — тестирование

---

## Концепции
- MTV: Model – Template – View
- DRY — не повторяться
- URL → view → шаблон → ответ
