# Получение acces и refresh токенов

POST запрос на
http://localhost:5000/oauth/token/

Headers: User-Agent - обязательно.   

В теле запроса необходимо передать дополнительные параметры:  
`json={"grant_type":"access_token", "email": "test@mail.ru", "password": "123"}`

В ответе вернётся JSON:   

```json
{
    "access_token": "{access_token}",
    "token_type": "bearer",
    "expires_in": 86400,
    "refresh_token": "{refresh_token}"
}
```
Если для клиента пользователя уже есть access_token, то метод вернет его.     
**Внимание:** Проверку на истекший токен результат не проходит.

**Ошибки**   
- 400 Bad Request – ошибка в параметрах запроса.

___


## Обновление пары access и refresh токенов
POST запрос на
http://localhost:5000/oauth/token/

В теле запроса необходимо передать дополнительные параметры:  
`json={"grant_type":"refresh_token", "refresh_token": "{refresh_token}"}`

Новая пара access_token и refresh_token будет выдана тому же user_agent пользователя, к которому была выдана предыдущая пара токенов.
 
Ответ будет идентичен ответу на получения токенов в первый раз:

```json
{
    "access_token": "{access_token}",
    "token_type": "bearer",
    "expires_in": 86400,
    "refresh_token": "{refresh_token}",
}
```
refresh_token можно использовать только один раз.

После получения новой пары access и refresh токенов, их необходимо использовать в дальнейших запросах в api и запросах на продление токена.