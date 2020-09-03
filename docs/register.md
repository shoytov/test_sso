# Регистрация нового пользователя
POST запрос на http://127.0.0.1:5000/oauth/register/

Headers: User-Agent - обязательно   
Токены создаются для user_agent пользователя, чтобы в дальнейшем пользователь мог запрашивать русурсы с этого клиента, однажды авторизовавшись.

**Тело запроса:**   
json={"name": "test", "email": "test@mail.ru", "password": "123"}

Если пользователь с таким email существует, будет ошибка:

```json
{
    "description": "User already exist!",
    "errors": [
        {
            "type": "bad request"
        }
    ]
}
```
Если регистрация прошла успешно - ответ будут токены:

```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTkwNDg5NzMsIm5iZiI6MTU5OTA0ODk3MywianRpIjoiMGNlNGI1M2ItZWE4Yi00NjViLThkMzctNzFhYWJjNGJiM2U1IiwiZXhwIjoxNTk5MTM1MzczLCJpZGVudGl0eSI6bnVsbCwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.r09o26SjxpWmtJQS4GneRdpK7z4JRaoYnVU4cuXtnjw",
    "expires_in": 86400,
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTkwNDg5NzMsIm5iZiI6MTU5OTA0ODk3MywianRpIjoiMWRjM2JlZGMtMzg3Ni00NmMwLTliMTItYjdiODI1ZDE3ZmYwIiwiZXhwIjoxNjAxNjQwOTczLCJpZGVudGl0eSI6bnVsbCwidHlwZSI6InJlZnJlc2gifQ.JvQaeG2O58EFctxf-QQXT_m7mT-2uzk7KG4AaylcWyg",
    "token_type": "bearer"
}
```

access_token дейтсвует 24 часа, потом надо запросить замену по refresh_token