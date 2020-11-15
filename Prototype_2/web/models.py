#from web import db #app, login_manager
import datetime
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .serve import app
# groups <> users: many to many
# groups <> messages: one to many
db = SQLAlchemy()

user_group = db.Table('user_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    def __init__(self, name, email, password):#, password!):
        self.name = name
        self.email = email
        self.password = password 
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': 3}).decode('utf-8')

    @staticmethod
    def verify_reset_token(self, token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(self.email)
    
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    createdAt = db.Column(DateTime, default=datetime.datetime.utcnow) # calc independently
    groups = db.relationship('Group', secondary='user_group', backref=db.backref('users'), lazy=True) # many to many w association table, lazy load

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String)
    userCount = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean)
    createdAt = db.Column(DateTime, default=datetime.datetime.utcnow) # calc independently
    messages = db.relationship('Message', backref='group', lazy=True)

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    success = db.Column(db.Boolean)
    reason = db.Column(db.String)
    createdAt = db.Column(DateTime, default=datetime.datetime.utcnow) # calc independently
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
