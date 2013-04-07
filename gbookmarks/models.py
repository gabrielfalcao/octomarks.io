# -*- coding: utf-8 -*-
import re
import hashlib
# from datetime import datetime
# from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy.sql.expression import desc, select, update, delete, insert

from gbookmarks.db import db, metadata, Model


def slugify(string):
    return re.sub(r'\W+', '-', string)


class User(Model):
    table = db.Table('gb_user', metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('github_id', db.Integer, nullable=False, unique=True),
        db.Column('gravatar_id', db.String(40), nullable=False, unique=True),
        db.Column('username', db.String(80), nullable=False, unique=True),
        db.Column('gb_token', db.String(40), nullable=False, unique=True),
        db.Column('email', db.String(100), nullable=False, unique=True),
    )

    def initialize(self):
        sha = hashlib.sha1()
        sha.update("github-bookmarks:")
        sha.update(self.username)
        self.gb_token = sha.hexdigest()

    def __repr__(self):
        return '<User %r, token=%r>' % (self.username, self.gb_token)

    @classmethod
    def create_from_github_user(cls, data):
        instance = cls(
            username=data.get('login'),
            github_id=data.get('id'),
            gravatar_id=data.get('gravatar_id'),
            email=data.get('email'),
        )
        return instance.save()


class Tag(Model):
    table = db.Table('gb_tag', metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('name', db.String(80), nullable=False, unique=True),
        db.Column('slug', db.String(80), nullable=False, unique=True),
    )

    def __init__(self, name):
        self.name = name.strip()
        self.slug = slugify(self.name)


class Bookmark(Model):
    table = db.Table('gb_bookmark', metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('url', db.Text, nullable=False),
    )

    def __init__(self, url):
        self.url = url.strip()


user_bookmark = db.Table('gb_user_bookmark', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, unique=True, nullable=False),
    db.Column('bookmark_id', db.Integer, unique=True, nullable=False),
)

bookmark_tags = db.Table('gb_bookmark_tags', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('tag_id', db.Integer, unique=True, nullable=False),
    db.Column('bookmark_id', db.Integer, unique=True, nullable=False),
)
