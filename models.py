from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SECRET_KEY'] = os.urandom(8).hex()
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(20),
                         nullable=False,
                         unique=True)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    full_name = db.Column(db.String(100),
                          unique=False,
                          nullable=False)
    dob = db.Column(db.String,
                          unique=False,
                          nullable=False)
    bio = db.Column(db.String(500),
                          unique=False,
                          nullable=False)
    password = db.Column(db.String(200),
                         unique=False,
                         nullable=False)
    date_registered = db.Column(db.String, 
                                nullable = False, 
                                default=datetime.now())
    posts = db.relationship('Post', backref=db.backref('author'))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model, UserMixin):
    """Model for managing post."""
    __tablename__ = 'post'

    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(db.String(200),
                      nullable=False,
                      unique=False)
    subtitle = db.Column(db.String(200),
                         unique=False,
                         nullable=True)
    body = db.Column(db.Text,
                     unique=False,
                     nullable=False)
    date_created = db.Column(db.String,
                             nullable=False,
                             default=datetime.now())
    tags = db.Column(db.String(50),
                     unique=False,
                     nullable=True)
    author_id = db.Column(db.Integer, 
                          db.ForeignKey('users.id'), 
                          nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.id'), 
                            nullable=False)

    def __repr__(self):
        return '<Post {}>'.format(self.id)



class Category(db.Model, UserMixin):
    """Model for categories of post."""
    __tablename__ = 'categories'

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String,
                     nullable=False,
                     unique=True)
    description = db.Column(db.Text,
                            unique=False,
                            nullable=False)
    members = db.relationship('Post', backref=db.backref('category'))

    def __repr__(self):
        return '<Category {}>'.format(self.name)

db.create_all()