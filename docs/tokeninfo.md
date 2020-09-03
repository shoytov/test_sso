# Проверка access-токена сервисом getme
http://localhost:5001/me   

GET запрос, обязательно передавать заголовок Authorization   
пример:
```http
GET /me HTTP/1.1
Accept: */*
Authorization: Bearer access_token
```
Ответ - JSON
___

# Проверка access-токена sso сервером
http://127.0.0.1:5000/oauth/tokeninfo/

Ответ - JSON с данными пользователя

```json
{
    "email": "test1@mail.ru",
    "name": "test"
}
```

___