import requests
from requests.exceptions import ConnectionError
import json
from flask import request, jsonify

from init import app


@app.route('/me', methods=['GET'])
def me():
    """ роут получает GET запрос, в заголовке которого должен быть передан параметр 
    Authorization: Bearer access_token
    access_token проходит валидацию в сервисе sso, в случае успеха - json с данными пользователя
    """
    
    header = request.headers.get('Authorization')
    token = ''

    if header:
        if header.find('Bearer') > -1:
            try:
                token = header.split(' ')[1]
            except IndexError:
                pass

    if token:
        # проверка через сервис
        url = 'http://localhost:5000/oauth/tokeninfo/'
        
        try:
            response = requests.get(url, headers=request.headers)
            response = json.loads(response.text)
        except ConnectionError:
            response = {
                "description": "The service is not available",
                "errors": [{"type":"forbidden"}],
                }            
    else:
        response = {
            "description": "Empty access token",
            "errors": [{"type":"forbidden"}],
            }

    return jsonify(response)