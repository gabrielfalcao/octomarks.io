# -*- coding: utf-8 -*-
import hashlib
from flask import config
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash

from gbookmarks.app import app


db = app.db

metadata = db.MetaData()

user = db.Table('gb_user', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('username', db.String(80), nullable=False, unique=True),
    db.Column('gb_token', db.String(40), nullable=False, unique=True),
)

tag = db.Table('gb_tag', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('name', db.String(80), nullable=False, unique=True),
    db.Column('slug', db.String(80), nullable=False, unique=True),
)

bookmark = db.Table('gb_bookmark', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('url', db.Text, nullable=False),
)

user_bookmark = db.Table('gb_user_bookmark', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, unique=True, nullable=False),
    db.Column('bookmark_id', db.Integer, unique=True, nullable=False),
)


class ORM(type):
    orm = config.Config()

    def __new__(cls, name, bases, attrs):
        cls.orm[name] = cls
        return super(ORM, cls).__new__(name, bases, attrs)


class Model(object):
    __metaclass__ = ORM


class User(Model):
    table = user

    def __init__(self, username):
        sha = hashlib.sha1()
        sha.update("github-bookmarks:")
        sha.update(username)
        self.username = username
        self.gb_token = sha.hexdigest()

    def __repr__(self):
        return '<User %r, token=%r>' % (self.username, self.gb_token)

class Tag(Model):
    table = tag

    def __init__(self, name):
        self.name = name.strip()
        self.slug = slugify(self.name)

class Bookmark(db.Model):
    table = bookmark

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))

    def __init__(self, url):
        self.url = url.strip()



def create_tables(db):
    db.create_all()
