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
    models = config.Config()

    def __new__(cls, name, bases, attrs):
        models.orm[name] = cls
        return super(ORM, cls).__new__(name, bases, attrs)


class Model(object):
    __metaclass__ = ORM

    @classmethod
    def find_by(cls, **kwargs):
        # TODO: implement
        import pdb;pdb.set_trace()

models = ORM.orm
