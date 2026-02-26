
Приложение для комментариев на Django.
Функциональность

- Древовидные комментарии с неограниченной вложенностью
- Сортировка по дате, имени, email
- Пагинация — 25 комментариев на страницу
- Прикрепление файлов: JPG/GIF/PNG (авторазмер до 320×240 через Celery) и TXT до 100 KB
- Защита от XSS — очистка HTML через `bleach`, разрешены только `<a>` `<code>` `<i>` `<strong>`
- CAPTCHA на форме
- Кэширование списка комментариев через Redis

## Стек

Python 3.13, Django 6, PostgreSQL, Redis, Celery, Pillow, bleach, docker-compose

## Запуск через Docker

```bash
git clone <repo_url>
cd task_comments_page
cp .env.example .env
docker-compose build
docker-compose up
```

Открыть: http://localhost:8000

## Локальный запуск без Docker

Нужны запущенные PostgreSQL и Redis.
В `.env.example` есть подсказка какие переменные поменять.
В .env нужно закомментировать переменные начинающиеся POSTGRES
и сменить REDIS_URL на закоментированный
В настройках закомментировать базу данных Postgres
и розкоментировать базу данных SQLite

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # заполнить своими значениями
docker run -d -p 6379:6379 redis
python manage.py migrate
python manage.py runserver

# в отдельном терминале
celery -A config worker -l info
```
Для создания суперюзера и входа в админ панель:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Кастомные решения

**`wait_for_db`** — management-команда которая ждёт готовности PostgreSQL перед запуском миграций. Используется в
`docker-compose.yaml` вместо `healthcheck`.

**`sanitizer.py`** — отдельный модуль для очистки HTML через bleach. Вызывается и в форме (`clean_text`) и в
предпросмотре.

**`signals.py`** — после сохранения комментария с изображением автоматически запускает задачу ресайза в Celery через
`post_save` сигнал.