import os

# db settings
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']

BASE_DIR = os.getcwd()

class Config(object):
    SECRET_KEY = 'qweSDad124fdfjhdsfhdshsd213SCcdsjfkn'
    SECURITY_PASSWORD_SALT = '213JJHgk&4253JGFh[=qjo09875->MBHsdf35'

    DEBUG = True

    CSRF_ENABLED = True

    SESSION_TYPE = 'sqlalchemy'
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)