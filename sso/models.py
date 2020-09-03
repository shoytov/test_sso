import hashlib
from datetime import timedelta
from passlib.hash import bcrypt
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_jwt_extended import create_access_token, create_refresh_token

from init import db, app


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(RoleMixin, db.Model):
    """ роль пользователя """
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
  
    def __str__(self):
        return self.name


class User(UserMixin, db.Model):
    """ модель пользователя """
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(254), nullable=False)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    user_client = db.relationship('UserClient', backref='user_client')
    
    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.name = kwargs.get('name')
        self.password = bcrypt.hash(kwargs.get('password'))

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        
        if not bcrypt.verify(password, user.password):
            raise Exception('Invalid password')
        return user


class UserClient(db.Model):
    """ клиенты пользователя (браузеры, мобильные приложения) """
    
    id = db.Column(db.Integer, primary_key=True)
    user_agent = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.user_agent = hashlib.md5(kwargs.get('user_agent').encode()).hexdigest()
    
    token = db.relationship('Token', backref='token')
    db.UniqueConstraint(user_agent, user_id)


class Token(db.Model):
    """ токены пользователя, которые выдаются на клиентское приложение, 
    с которого пользователь запрашивает ресурс """
    
    id = db.Column(db.Integer, primary_key=True)
    user_client_id = db.Column(db.Integer, db.ForeignKey('user_client.id'), nullable=False)
    access_token = db.Column(db.Text(), nullable=False)
    refresh_token = db.Column(db.Text(), nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, user_client_id):
        self.user_client_id = user_client_id
        self.access_token = create_access_token(identity=self.id, expires_delta=timedelta(1))
        self.refresh_token = create_refresh_token(identity=self.id)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)