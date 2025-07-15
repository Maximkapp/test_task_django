# Тестовое задание

Django-приложение для размещения, просмотра и обмена объявлений. Минимальный MVP с базовой функциональностью и полной поддержкой Docker.

## 🚀 Возможности
- Регистрация пользователя
- Добавление, редактирование, удаление, поиск объявлений
- Поиск объявлений по фильтрам
- Обмен товаров между пользователями
- Статические файлы и шаблоны подключены
- SQLite используется как БД
- Готовая контейнеризация: Docker + Docker Compose

## 🛠️ Технологии

- Python 3.11+
- Django 5.x
- SQLite
- Docker & Docker Compose

## 📦 Быстрый старт (через Docker)

```bash
# Клонируем проект
git clone https://github.com/Maximkapp/test_task_django.git
# Переходим в папку с проектом
cd test_task
# Создаём файл .env

type nul > .env
# или
touch .env
  
# Пример файла :
DEBUG=True
SECRET_KEY='django-insecure-c4wl##a!wf26-+atig@%ul4nmh6e^_n_gan2u4j^qy!+5t3ied'
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1


# Делаем миграции
docker-compose run app python manage.py migrate

# Собираем и запускаем контейнер
docker-compose up --build
