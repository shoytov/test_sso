import hashlib
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from flask_jwt_extended import jwt_required

from init import db
from models import User, UserClient, Token

oauth = Blueprint('oauth', __name__)


@oauth.route('tokeninfo/', methods=['GET'])
@jwt_required
def tokeninfo():
    """ проверка токена на валидность 
        токен передается в заголовке Authorization
    """
    access_token = request.headers.get('Authorization').split(' ')[1]
    token = Token.query.filter(Token.access_token == access_token)
    if token.count() > 0:
        user = User.query.filter(User.id == UserClient.query.filter(
            UserClient.id == token.one().user_client_id).one().user_id).one()

        response = {
            "email": user.email,
            "name": user.name,
            }
    else:
        response = {
            "description": "Token not found",
            "errors": [{"type":"forbidden"}],
            }            

    return jsonify(response)


def generate_new_token(user_id: int, user_agent: str) -> dict:
    """ процедура генерации новых access и refresh токенов для клиента пользователя """
    user_client = UserClient(**{'user_id': user_id, 'user_agent': user_agent})
    db.session.add(user_client)
    db.session.commit()

    token = Token(user_client.id)
    db.session.add(token)
    db.session.commit()

    result = {
        "access_token": token.access_token,
        "token_type": "bearer",
        "expires_in": 86400,
        "refresh_token": token.refresh_token,
    }  

    return result  


@oauth.route('register/', methods=['POST'])
def register():
    """ регистрация пользователя 
    возвращает access и refresh токены в случе успеха, 
    bad request - в случае неудачи
    """

    user_agent = request.headers.get('User-Agent')
    if user_agent:
        try:
            params = request.json
            user = User(**params)
            db.session.add(user)
            db.session.commit()

            response = generate_new_token(user.id, user_agent)
        except IntegrityError:
            response = {
                "description": "User already exist!",
                "errors": [{"type":"bad request"}],
                }
    else:
        response = {
            "description": "User-agent is required",
            "errors": [{"type":"bad request"}],
            }

    return jsonify(response)


def make_access_token(email: str, password: str, user_agent: str) -> dict:
    """ формирование access_tokena для зарегистрированного пользователя
    В случае, если User-Agent пользователя уже имеет токен, будет возвращен он
    """

    try:
        user = User.authenticate(email, password)
    except Exception:
        response = {
            "description": "User not found!",
            "errors": [{"type":"bad request"}],
        }
    else:
        user_client = UserClient.query.filter(and_(UserClient.user_agent == hashlib.md5(user_agent.encode()).hexdigest(), UserClient.user_id == user.id))

        if user_client.count() > 0:
            token = Token.query.filter(and_(Token.user_client_id == user_client.first().id, Token.used == False))

            if token.count() > 0:
                response = {
                    "access_token": token.first().access_token,
                    "token_type": "bearer",
                    "expires_in": 86400,
                    "refresh_token": token.first().refresh_token,
                }
            else:
                # токена для клиента пользователя нет - генерируем новый токен
                response = generate_new_token(user.id, user_agent)        
        else:
            response = generate_new_token(user.id, user_agent)
    
    return response


def make_refresh_token(refresh_token: str) -> dict:
    """ формирование нового access_token по refresh_token """
    
    token = Token.query.filter(and_(Token.refresh_token == refresh_token, Token.used == False))

    if token.count() > 0:
        token = token.first()

        new_token = Token(token.user_client_id)
        db.session.add(new_token)
        db.session.commit()

        token.used = True
        db.session.add(token)
        db.session.commit()        

        result = {
            "access_token": new_token.access_token,
            "token_type": "bearer",
            "expires_in": 86400,
            "refresh_token": new_token.refresh_token,
        }          
    else:
        result = {
            "description": "Refresh token not found or it was used",
            "errors": [{"type":"bad request"}],            
        }
    
    return result


@oauth.route('token/', methods=['POST'])
def token():
    """ выдача токена пользователю """

    params = request.json

    user_agent = request.headers.get('User-Agent')
    if user_agent:
        if 'grant_type' in params.keys():
            case = {
                'access_token': make_access_token(params.get('email'), params.get('password'), user_agent),
                'refresh_token': make_refresh_token(params.get('refresh_token'))
            }
            response = case.get(params.get('grant_type'))
        else:
            response = {
                "description": "grant_type parameter is missed",
                "errors": [{"type":"bad request"}],
                }                  
    else:
        response = {
            "description": "User-Agent header is missed",
            "errors": [{"type":"bad request"}],
            }            

    return jsonify(response)
