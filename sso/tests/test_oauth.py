import os
import unittest

from app import app
from init import db
from config import BASE_DIR
from models import Token

class TestOauth(unittest.TestCase):
    def setUp(self):
        db_path = os.path.join(BASE_DIR, 'test.db')
        
        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
        self.app = app.test_client()
        db.create_all()
        self.db = db


    def register(self):
        """ запуск регистрации нового пользователя для создания тестовых данных """
        
        headers = {'User-Agent': 'MyApp ver 1', 'Content-Type': 'application/json'}
        data = {"name": "test", "email": "test@mail.ru", "password": "123"}

        response = self.app.post('/oauth/register/', headers=headers, json=data)
        return response


    def test_register(self):
        response = self.register()

        self.assertEqual(200, response.status_code)
        self.assertEqual(str, type(response.json['access_token']))


    def test_tokeninfo(self):
        self.register()

        token = Token.query.filter(Token.used == False).first()
        token_header = 'Bearer {}'.format(token.access_token)
        headers = {'Authorization': token_header}
        
        response = self.app.get('/oauth/tokeninfo/', headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(str, type(response.json['email']))
        self.assertEqual(str, type(response.json['name']))


    def test_get_access_token(self):
        self.register()

        headers = {'User-Agent': 'MyApp ver 1', 'Content-Type': 'application/json'}
        data = {"grant_type":"access_token", "email": "test@mail.ru", "password": "123"}

        response = self.app.post('/oauth/token/', headers=headers, json=data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(str, type(response.json['access_token']))


    def test_get_access_token_by_refresh_token(self):
        self.register()

        token = Token.query.filter(Token.used == False).first()
        headers = {'User-Agent': 'MyApp ver 1', 'Content-Type': 'application/json'}
        data = {"grant_type":"refresh_token", "refresh_token": "{}".format(token.refresh_token)}

        response = self.app.post('/oauth/token/', headers=headers, json=data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(str, type(response.json['access_token']))        