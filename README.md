# question_test_task
## Устоновка и запуск 
1. Склонировать репозиторий
2. Перейти в директорию проекта
```
cd question_project
```
3. Создать `.env` файл в корне проекта
```
# Django
DEBUG=True
SECRET_KEY=django-secret-key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# PostgreSQL
POSTGRES_DB=question_db
POSTGRES_USER=question_user
POSTGRES_PASSWORD=secret
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

4. Запуск приложение в контейнерах

```
docker compose up --build
```

5.Выполнить миграции:

```
docker compose exec web python manage.py migrate
```

## Запуск тестов 
```
docker compose exec web pytest
```

## Примеры запросов 
### 1. Создание вопроса
- **Метод** `POST`
- **URL** `http://127.0.0.1:8000/api/questions/`
- **Body**
  
  ```
  {
    "text": "Вопрос?"
  }
  ```
  **Пример ответа**
    ```
      {
        "id": 1,
        "text": "Вопрос?",
        "created_at": "2025-09-01T05:06:12.104767Z"
      }
     ```
### 2. Получение всех вопросов
- **Метод** `GET`
- **URL** `http://127.0.0.1:8000/api/questions/`
**Пример ответа**
  
   ```
   [
      {
          "id": 1,
          "text": "Вопрос",
          "created_at": "2025-09-01T04:26:13.350209Z"
      },
      {
          "id": 2,
          "text": "Вопрос 1?",
          "created_at": "2025-09-01T05:06:12.104767Z"
      },
      {
          "id": 3,
          "text": "Вопрос 2 ?",
          "created_at": "2025-09-01T05:09:28.871368Z"
      },
      {
          "id": 4,
          "text": "Вопрос 3 ?",
          "created_at": "2025-09-01T05:09:35.153920Z"
      }
  ]
   ```
### 3. Получение вопроса с ответами
- **Метод** `GET`
- **URL** `http://127.0.0.1:8000/api/questions/1/`
**Пример ответа**
  
   ```
  {
      "id": 1,
      "text": "Вопрос",
      "created_at": "2025-09-01T04:26:13.350209Z",
      "answers": [
          {
              "id": 1,
              "text": "ответ 1 ?",
              "created_at": "2025-09-01T05:10:25.662338Z"
          },
          {
              "id": 2,
              "text": "ответ 2",
              "created_at": "2025-09-01T05:10:34.257116Z"
          },
          {
              "id": 3,
              "text": "ответ 3",
              "created_at": "2025-09-01T05:10:38.417221Z"
          }
      ]
  }
   ```
### 4. Удаление вопроса с ответами
- **Метод** `DELETE`
- **URL** `http://127.0.0.1:8000/api/questions/1/`

### 5. Создание ответа
- **Метод** `POST`
- **URL** `http://127.0.0.1:8000/api/questions/2/answers/`
- **Body**
  
  ```
  {
    "text": "ответ"
  }
  ```
  **Пример ответа**
     ```
      {
        "id": 4,
        "text": "ответ",
        "created_at": "2025-09-01T05:15:47.620563Z"
    }
     ```
### 5. Получение ответа
- **Метод** `GET`
- **URL** `http://127.0.0.1:8000/api/answers/4/`
**Пример ответа**
  
   ```
    {
      "id": 4,
      "text": "ответ",
      "created_at": "2025-09-01T05:15:47.620563Z"
    }
   ```
### 5. Ужаление ответа
- **Метод** `DELETE`
- **URL** `http://127.0.0.1:8000/api/answers/4/`

