# Task Tracker (Django + DRF)

Backend для трекинга проектов, задач и комментариев на Django REST Framework.

## Требования

- Python 3.11+
- Windows PowerShell

## Установка

1. Создать и активировать виртуальное окружение (если `.venv` уже есть, просто активируйте):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Установить зависимости:

```powershell
pip install -r .\requirements.txt
```

## Переменные окружения

Проект читает `SECRET_KEY` из `.env`.

Пример `.env`:

```env
SECRET_KEY=your-secret-key
```

Сгенерировать `SECRET_KEY` можно так:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Миграции и запуск

Команды выполняются из каталога `Task_Tracker` (там лежит `manage.py`):

```powershell
cd .\Task_Tracker
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

По умолчанию сервер поднимется на `http://127.0.0.1:8000/`.

## Документация API (Swagger/ReDoc)

- OpenAPI schema: `GET /api/schema/`
- Swagger UI: `GET /api/docs/swagger/`
- ReDoc: `GET /api/docs/redoc/`

## Аутентификация

Отдельного API-эндпоинта регистрации/логина сейчас нет. Пользователей можно создать через Django admin или `createsuperuser`.

DRF по умолчанию поддерживает Basic Auth, поэтому для запросов через `curl` можно использовать:

```powershell
curl -u "email@example.com:password" http://127.0.0.1:8000/api/projects/
```

Также можно авторизоваться в админке `GET /admin/` и открывать Swagger/ReDoc в том же браузере (сессионная cookie будет отправляться автоматически).

## Эндпоинты

Базовый префикс: `/api/`

### Projects

- `GET /api/projects/` список проектов, где вы участник
- `POST /api/projects/` создать проект (создатель автоматически добавляется в участники с ролью `owner`)
- `GET /api/projects/{id}/` детали проекта (только участники)
- `PATCH /api/projects/{id}/`, `DELETE /api/projects/{id}/` (только владелец)

Участники проекта:

- `GET /api/projects/{id}/members/` список участников
- `POST /api/projects/{id}/members/` добавить участника (только владелец)
  - body: `{ "user": <user_id>, "role": "member" }` (роль можно не передавать, по умолчанию будет `member`)
- `DELETE /api/projects/{id}/members/{user_id}/` удалить участника (только владелец, владельца удалить нельзя)

### Tasks

- `GET /api/tasks/` список задач из проектов, где вы участник
- `POST /api/tasks/` создать задачу
- `GET /api/tasks/{id}/`, `PATCH /api/tasks/{id}/`, `DELETE /api/tasks/{id}/`

Фильтрация задач через query params:

- `project=<project_id>`
- `status=new|in_progress|review|done`
- `priority=low|medium|high|urgent`
- `assignee=<user_id>`
- `deadline_from=YYYY-MM-DD`
- `deadline_to=YYYY-MM-DD`

Пример:

```powershell
curl -u "email@example.com:password" "http://127.0.0.1:8000/api/tasks/?project=1&status=in_progress&deadline_to=2026-12-31"
```

Пагинация:

- `page=<n>` (PageNumberPagination)

### Comments

- `GET /api/comments/` комментарии по задачам из ваших проектов
- `POST /api/comments/` создать комментарий
- `GET /api/comments/{id}/`, `PATCH /api/comments/{id}/`, `DELETE /api/comments/{id}/`

Пример создания комментария:

```powershell
curl -u "email@example.com:password" -H "Content-Type: application/json" `
  -d "{ \"task\": 1, \"text\": \"Уточните критерии приемки\" }" `
  http://127.0.0.1:8000/api/comments/
```
