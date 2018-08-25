import datetime
from flaskr.db import db
from sqlalchemy.orm import aliased


class Reply(db.Model):
    __tablename__ = 'reply'
    __table_args = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    reply_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    reply_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    reply_text = db.Column(db.String(200), nullable=False)

    def __init__(self, author_id, post_id, reply_text):
        self.author_id = author_id
        self.post_id = post_id
        self.reply_text = reply_text
        

class Post(db.Model):

    __tablename__ = 'post'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer)
   
    post_created = db.Column(db.DateTime, default=datetime.datetime.now())
    theme_id = db.Column(db.Integer, nullable=False)
    post_title = db.Column(db.String(128), nullable=False)
    post_body = db.Column(db.Text, nullable=False)

    def __init__(self, author_id, theme_id, post_title, post_body):
        self.author_id = author_id
        self.theme_id = theme_id
        self.post_title = post_title
        self.post_body = post_body


class Theme(db.Model):

    __tablename__ = 'theme'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    theme_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, nullable=False)
    theme_created = db.Column(db.DateTime, default=datetime.datetime.now())
    theme_text = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, author_id, theme_text):
        self.author_id = author_id
        self.theme_text = theme_text 


class User(db.Model):

    __tablename__ = 'user'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    user_password = db.Column(db.String(120), nullable=False)
    user_sign = db.Column(db.Integer, nullable=False)

    def __init__(self, username, userpassward, user_sign):
        self.username = username
        self.user_password = userpassward
        self.user_sign = user_sign




