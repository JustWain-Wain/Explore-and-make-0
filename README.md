# Task Tracker API

Backend для управления пользователями, проектами, задачами и комментариями на Django REST Framework.

## Что есть в проекте

Проект состоит из трех приложений:

- `apps.users` - кастомная модель пользователя на базе `AbstractUser`
- `apps.projects` - проекты и состав участников
- `apps.tasks` - задачи и комментарии

API построено на `ModelViewSet` и `DefaultRouter`. Документация схемы отдается через встроенный OpenAPI-генератор DRF.

## Текущий стек

- Python 3.11+
- Django 6
- Django REST Framework
- SQLite
- Token Authentication

## Структура данных

### Пользователь

Модель `User` расширяет `AbstractUser` и использует `email` как поле входа:

- `id`
- `username`
- `email`
- `first_name`
- `last_name`
- `middle_name`
- `position`
- `password`

Особенности:

- `email` уникален
- `USERNAME_FIELD = "email"`
- пароль в API доступен только на запись

### Проект

Модель `Project` хранит:

- `id`
- `name`
- `description`
- `creator`
- `created_at`
- `changed_at`
- `deadline`

Связь с пользователями реализована через промежуточную модель `ProjectMember`.

### Участник проекта

Модель `ProjectMember` хранит:

- `id`
- `project`
- `user`
- `role`

Роли:

- `owner`
- `member`

Ограничения:

- один и тот же пользователь не может быть добавлен в один проект дважды

### Задача

Модель `Task` хранит:

- `id`
- `name`
- `description`
- `status`
- `priority`
- `deadline`
- `created_at`
- `changed_at`
- `project`
- `author`
- `assignee`

Статусы:

- `new`
- `in_progress`
- `review`
- `done`

Приоритеты:

- `low`
- `medium`
- `high`
- `urgent`

### Комментарий

Модель `Comment` хранит:

- `id`
- `task`
- `author`
- `text`
- `created_at`
- `changed_at`

## Правила доступа

Ниже описано фактическое поведение API по коду.

### Пользователи

- все методы `users` требуют авторизации
- обычный пользователь видит только самого себя
- `staff` пользователь видит всех пользователей
- отдельного ограничения на изменение или удаление пользователя в `UserViewSet` не задано, поэтому после прохождения `IsAuthenticated` объектные операции не блокируются дополнительной permission-логикой

### Проекты

- список проектов содержит только те проекты, где пользователь состоит в участниках
- читать конкретный проект может только его участник
- изменять и удалять проект может только `owner`
- при создании проекта текущий пользователь автоматически становится `creator` и участником с ролью `owner`

### Участники проекта

- получить список участников проекта может участник проекта
- добавлять и удалять участников может только `owner`
- удалить владельца из собственного проекта нельзя

### Задачи

- список задач содержит только задачи из проектов, где пользователь состоит в участниках
- читать задачу может любой участник проекта
- создавать задачу может любой участник проекта, если переданный `assignee` входит в этот же проект
- автор задачи может изменять и удалять задачу
- исполнитель задачи может частично менять задачу через `PATCH`, если запрос затрагивает `status` или `priority`

Важно:

- если исполнитель отправляет `PATCH` c полями `status` или `priority`, permission допускает запрос
- но если в том же `PATCH` будут другие поля, сериализатор тоже попытается их обновить
- в README ниже процедуры описаны так, чтобы не опираться на спорное поведение и разделять обновление статуса и редактирование самой задачи

### Комментарии

- список комментариев содержит только комментарии к задачам из проектов, где пользователь состоит в участниках
- читать комментарии может любой участник проекта
- создавать комментарии может любой участник проекта
- изменять и удалять комментарий может только автор комментария

## Установка

Команды ниже выполняются из корня репозитория.

1. Создать виртуальное окружение:

```powershell
python -m venv .venv
```

2. Активировать его:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Установить зависимости:

```powershell
pip install -r .\requirements.txt
```

4. Создать файл `.env` в корне репозитория:

```env
SECRET_KEY=your-secret-key
```

5. Сгенерировать ключ при необходимости:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

6. Перейти в каталог проекта Django:

```powershell
cd .\Task_Tracker
```

7. Выполнить миграции:

```powershell
python manage.py migrate
```

8. Создать суперпользователя:

```powershell
python manage.py createsuperuser
```

9. Запустить сервер:

```powershell
python manage.py runserver
```

Сервер по умолчанию доступен по адресу `http://127.0.0.1:8000/`.

## Документация API

- OpenAPI schema: `GET /api/schema/`
- Swagger UI: `GET /api/docs/swagger/`
- ReDoc: `GET /api/docs/redoc/`

## Аутентификация

В `REST_FRAMEWORK` включена только `TokenAuthentication`:

```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication'
]
```

- для запросов к защищенным endpoint нужно передавать заголовок `Authorization: Token <token>`
- `BasicAuth` в текущей конфигурации не используется
- endpoint для выдачи токена в `urls.py` не подключен

### Как получить токен в текущем состоянии проекта

Вариант 1. Через Django shell:

```powershell
cd .\Task_Tracker
python manage.py shell
```

```python
from apps.users.models import User
from rest_framework.authtoken.models import Token

user = User.objects.get(email="admin@example.com")
token, _ = Token.objects.get_or_create(user=user)
print(token.key)
```

Вариант 2. Через Django admin, если там зарегистрировать модель токенов отдельно.

Сейчас в проекте это не настроено автоматически.

### Пример заголовка авторизации

```http
Authorization: Token your_token_here
```

### Пример запроса через PowerShell

```powershell
$headers = @{
  Authorization = "Token your_token_here"
}

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users/" -Headers $headers
```

## Общие правила работы API

Базовый префикс всех endpoint: `/api/`

Пагинация:

- используется `PageNumberPagination`
- размер страницы: `10`
- для перехода по страницам используется query-параметр `page`

Типовой ответ списка:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": []
}
```

Если у пользователя нет доступа к объекту:

- обычно возвращается `403 Forbidden`
- если объект не найден в доступной выборке, возможен `404 Not Found`

## Процедуры взаимодействия с API

Ниже описаны рекомендуемые рабочие сценарии в том порядке, в котором ими обычно пользуются.

### 1. Создание пользователя

Endpoint:

- `POST /api/users/`

Тело запроса:

```json
{
  "username": "ivanov",
  "email": "ivanov@example.com",
  "password": "StrongPassword123",
  "first_name": "Иван",
  "last_name": "Иванов",
  "middle_name": "Иванович",
  "position": "Backend Developer"
}
```

Что делает API:

- создает пользователя
- хеширует пароль через `create_user`

Замечание:

- сам endpoint находится под `IsAuthenticated`, поэтому создать пользователя анонимно нельзя
- на практике новых пользователей сейчас удобнее создавать через `createsuperuser`, admin или уже авторизованным администратором через API

### 2. Получение данных пользователя

Endpoint:

- `GET /api/users/`
- `GET /api/users/{id}/`

Правила:

- обычный пользователь видит только себя
- `staff` пользователь видит всех

Пример:

```powershell
$headers = @{ Authorization = "Token your_token_here" }
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users/" -Headers $headers
```

### 3. Создание проекта

Endpoint:

- `POST /api/projects/`

Тело запроса:

```json
{
  "name": "CRM Migration",
  "description": "Перенос задач в новую систему",
  "deadline": "2026-12-31T18:00:00+05:00"
}
```

Что делает API:

- создает проект
- записывает текущего пользователя в `creator`
- автоматически добавляет его в участники с ролью `owner`

Валидации:

- `name` должен содержать минимум 3 символа
- `deadline` не может быть в прошлом

### 4. Получение списка проектов

Endpoint:

- `GET /api/projects/`

Возвращает:

- только те проекты, где текущий пользователь является участником

Пример:

```powershell
$headers = @{ Authorization = "Token your_token_here" }
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/projects/" -Headers $headers
```

### 5. Изменение или удаление проекта

Endpoint:

- `PATCH /api/projects/{id}/`
- `DELETE /api/projects/{id}/`

Правила:

- доступно только владельцу проекта

Пример частичного обновления:

```powershell
$headers = @{
  Authorization = "Token your_token_here"
  "Content-Type" = "application/json"
}

$body = @{
  description = "Обновленное описание проекта"
} | ConvertTo-Json

Invoke-RestMethod -Method Patch -Uri "http://127.0.0.1:8000/api/projects/1/" -Headers $headers -Body $body
```

### 6. Получение участников проекта

Endpoint:

- `GET /api/projects/{id}/members/`

Возвращает список записей `ProjectMember`, а не только пользователей. У каждой записи есть:

- `id`
- `project`
- `user`
- `role`

Пример:

```powershell
$headers = @{ Authorization = "Token your_token_here" }
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/projects/1/members/" -Headers $headers
```

### 7. Добавление участника в проект

Endpoint:

- `POST /api/projects/{id}/members/`

Кто может:

- только `owner`

Тело запроса:

```json
{
  "user": 3,
  "role": "member"
}
```

Особенности:

- `role` необязателен, по умолчанию будет `member`
- нельзя добавить того же пользователя в проект повторно

Рекомендуемая процедура:

1. Создать или найти пользователя.
2. Создать проект.
3. Добавить пользователя в проект через `/members/`.
4. Только после этого назначать его исполнителем задач в этом проекте.

### 8. Удаление участника из проекта

Endpoint:

- `DELETE /api/projects/{id}/members/{user_id}/`

Кто может:

- только `owner`

Ограничения:

- удалить владельца проекта нельзя

### 9. Создание задачи

Endpoint:

- `POST /api/tasks/`

Тело запроса:

```json
{
  "name": "Подготовить ТЗ",
  "description": "Собрать требования от отдела продаж",
  "status": "new",
  "priority": "high",
  "deadline": "2026-10-01T12:00:00+05:00",
  "project": 1,
  "assignee": 3
}
```

Что делает API:

- сохраняет автора автоматически из `request.user`

Валидации:

- `name` минимум 3 символа
- `deadline` не может быть в прошлом
- `assignee` должен быть участником выбранного проекта

Рекомендуемая процедура:

1. Получить `project_id`.
2. Убедиться, что исполнитель уже добавлен в проект.
3. Создать задачу.

### 10. Получение списка задач

Endpoint:

- `GET /api/tasks/`

Возвращает:

- только задачи из проектов, где текущий пользователь является участником

Поддерживаемые фильтры:

- `project=<project_id>`
- `status=new|in_progress|review|done`
- `priority=low|medium|high|urgent`
- `assignee=<user_id>`
- `deadline_from=YYYY-MM-DD`
- `deadline_to=YYYY-MM-DD`
- `page=<n>`

Пример:

```powershell
$headers = @{ Authorization = "Token your_token_here" }
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/tasks/?project=1&status=in_progress&deadline_to=2026-12-31" -Headers $headers
```

### 11. Обновление задачи автором

Endpoint:

- `PATCH /api/tasks/{id}/`
- `PUT /api/tasks/{id}/`

Кто может:

- автор задачи

Когда использовать:

- изменить описание
- переназначить исполнителя
- поменять дедлайн
- скорректировать приоритет
- полностью заменить данные задачи

Безопасная рекомендация:

- все содержательные изменения задачи, кроме быстрой смены статуса исполнителем, лучше выполнять от имени автора задачи

### 12. Быстрое обновление статуса или приоритета исполнителем

Endpoint:

- `PATCH /api/tasks/{id}/`

Кто может:

- `assignee`, если меняет `status` и или `priority`

Рекомендуемое тело запроса:

```json
{
  "status": "review"
}
```

или

```json
{
  "priority": "urgent"
}
```

Практическое правило:

- исполнителю лучше отправлять `PATCH` только с полями `status` и `priority`
- не смешивать это обновление с другими полями в одном запросе

### 13. Удаление задачи

Endpoint:

- `DELETE /api/tasks/{id}/`

Кто может:

- только автор задачи

### 14. Создание комментария к задаче

Endpoint:

- `POST /api/comments/`

Тело запроса:

```json
{
  "task": 1,
  "text": "Нужно уточнить критерии приемки"
}
```

Что делает API:

- автоматически записывает текущего пользователя в `author`

Кто может:

- любой участник проекта, к которому относится задача

Валидации:

- текст не должен быть пустым
- пользователь должен состоять в проекте этой задачи

### 15. Получение списка комментариев

Endpoint:

- `GET /api/comments/`

Возвращает:

- комментарии только по тем задачам, которые находятся в проектах текущего пользователя

### 16. Обновление и удаление комментария

Endpoint:

- `PATCH /api/comments/{id}/`
- `PUT /api/comments/{id}/`
- `DELETE /api/comments/{id}/`

Кто может:

- только автор комментария

## Готовые сценарии работы

### Сценарий 1. Запуск проекта с нуля

1. Создать администратора через `createsuperuser`.
2. Получить или создать токен для администратора.
3. Создать пользователей команды.
4. Создать проект.
5. Добавить участников в проект через `/api/projects/{id}/members/`.
6. Создать задачи и назначить исполнителей.
7. Отслеживать статус через `/api/tasks/`.
8. Обсуждать задачи через `/api/comments/`.

### Сценарий 2. Работа исполнителя

1. Получить свой список проектов через `/api/projects/`.
2. Получить свои задачи через `/api/tasks/?assignee=<user_id>`.
3. Перевести задачу в `in_progress`.
4. После завершения перевести задачу в `review` или `done`.
5. При необходимости оставить комментарий через `/api/comments/`.

### Сценарий 3. Работа владельца проекта

1. Создать проект.
2. Добавить участников.
3. Проверить список участников через `/members/`.
4. Контролировать сроки задач через фильтр `deadline_to`.
5. При необходимости удалить участника или скорректировать проект.

## Примеры запросов c `curl`

### Получить список проектов

```bash
curl -X GET "http://127.0.0.1:8000/api/projects/" \
  -H "Authorization: Token your_token_here"
```

### Создать проект

```bash
curl -X POST "http://127.0.0.1:8000/api/projects/" \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CRM Migration",
    "description": "Перенос задач в новую систему",
    "deadline": "2026-12-31T18:00:00+05:00"
  }'
```

### Добавить участника

```bash
curl -X POST "http://127.0.0.1:8000/api/projects/1/members/" \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "user": 3,
    "role": "member"
  }'
```

### Создать задачу

```bash
curl -X POST "http://127.0.0.1:8000/api/tasks/" \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Подготовить ТЗ",
    "description": "Собрать требования от отдела продаж",
    "status": "new",
    "priority": "high",
    "deadline": "2026-10-01T12:00:00+05:00",
    "project": 1,
    "assignee": 3
  }'
```

### Обновить статус задачи

```bash
curl -X PATCH "http://127.0.0.1:8000/api/tasks/1/" \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "review"
  }'
```

### Создать комментарий

```bash
curl -X POST "http://127.0.0.1:8000/api/comments/" \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "task": 1,
    "text": "Нужно уточнить критерии приемки"
  }'
```
