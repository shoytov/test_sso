import os
import unittest
import sys

from app import app


class TestOauth(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client() 
    
    def test_me(self):
        token = input('insert access_token: ')
        token_header = 'Bearer {}'.format(token)
        headers = {'Authorization': token_header}
        
        response = self.app.get('/me', headers=headers)
        self.assertEqual(200, response.status_code)