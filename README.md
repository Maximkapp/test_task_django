# Тестовое задание

Django-приложение для размещения, просмотра и обмена объявлений. Минимальный MVP с базовой функциональностью и полной поддержкой Docker.

##  Возможности
- Регистрация пользователя
- Добавление, редактирование, удаление, поиск объявлений
- Поиск объявлений по фильтрам
- Обмен товаров между пользователями
- Статические файлы и шаблоны подключены
- SQLite используется как БД
- Готовая контейнеризация: Docker + Docker Compose

## Технологии

- Python 3.11+
- Django 5.x
- SQLite
- Docker & Docker Compose

## Быстрый старт (через Docker)

```bash
# Клонируем проект
git clone https://github.com/Maximkapp/test_task_django.git
# Переходим в папку с проектом
cd test_task
# Создаём файл .env

# Пример файла :
DEBUG=
SECRET_KEY=
DJANGO_ALLOWED_HOSTS=


# Делаем миграции
docker-compose run app python manage.py migrate

# Собираем и запускаем контейнер
docker-compose up --build
