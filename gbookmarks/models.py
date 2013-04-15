# -*- coding: utf-8 -*-
import re
import ejson as json
import ejson.serializers
import hashlib
from datetime import datetime
# from werkzeug import generate_password_hash, check_password_hash
import logging

logger = logging.getLogger('gbookmarks.models')

from gbookmarks.db import db, metadata, Model
from gbookmarks.core import RepoInfo


def slugify(string):
    return re.sub(r'\W+', '-', string)


def now():
    return datetime.now()


class User(Model):
    table = db.Table('gb_user', metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('github_id', db.Integer, nullable=False, unique=True),
        db.Column('github_token', db.String(256), nullable=True),
        db.Column('gravatar_id', db.String(40), nullable=False, unique=True),
        db.Column('username', db.String(80), nullable=False, unique=True),
        db.Column('gb_token', db.String(40), nullable=False, unique=True),
        db.Column('email', db.String(100), nullable=False, unique=True),
        db.Column('created_at', db.DateTime, default=now),
        db.Column('updated_at', db.DateTime, default=now),
    )

    def initialize(self):
        sha = hashlib.sha1()
        sha.update("github-bookmarks:")
        sha.update(self.username)
        self.gb_token = sha.hexdigest()

    def __repr__(self):
        return '<User %r, token=%r>' % (self.username, self.gb_token)

    def save_bookmark(self, uri):
        # TODO: take project, languages and all the other data that
        # will be fetched by the view, so you can have more
        # information.
        info = RepoInfo(uri.strip())
        if info:
            return Bookmark.get_or_create(user_id=self.id, url=info.remount())

    def get_bookmarks(self):
        return Bookmark.find_by(user_id=self.id)

    @classmethod
    def create_from_github_user(cls, data):
        login = data.get('login')
        instance = cls.create(
            username=login,
            github_id=data.get('id'),
            gravatar_id=data.get('gravatar_id'),
            email=data.get('email', "{0}@github-bookmarks.com".format(login)),
            github_token=data.get('github_token')
        )
        logger.info("user %d created: %s", instance.id, instance.email)

        return instance

    @classmethod
    def get_or_create_from_github_user(cls, data):
        instance = cls.find_one_by(username=data['login'])
        if not instance:
            return cls.create_from_github_user(data)

        return instance


class Tag(Model):
    table = db.Table('gb_tag', metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('name', db.String(80), nullable=False, unique=True),
        db.Column('slug', db.String(80), nullable=False, unique=True),
        db.Column('created_at', db.DateTime, default=now),
        db.Column('updated_at', db.DateTime, default=now),
    )

    def preprocess(self, data):
        name = data.get('name')
        if name:
            cleaned_name = re.sub(r'\s+', ' ', name).lower()
            data['name'] = cleaned_name
            data['slug'] = slugify(cleaned_name)

        return data


class Bookmark(Model):
    table = db.Table('gb_bookmark', metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('user_id', db.Integer),
        db.Column('url', db.Text, nullable=False),
        db.Column('created_at', db.DateTime, default=now),
        db.Column('updated_at', db.DateTime, default=now),
    )
    regexes = [
        re.compile(r'github.com/(?P<owner>[^/]+)/(?P<project>[^/]+)'),
        re.compile(r'(?P<owner>[^.]+).github.io/(?P<project>[^/]+)'),
    ]

    @classmethod
    def get_most_bookmarked(cls, limit=5):
        field = cls.table.c
        q = (db.select([
            field.url,
            db.func.count('*')
        ])
            .group_by(field.url)
            .order_by(db.desc(db.func.count('*')))
            .limit(limit))

        conn = cls.get_connection()
        res = conn.execute(q)
        return [(RepoInfo(url), count) for url, count in res.fetchall()]

    def add_tag(self, name):
        tag = Tag.get_or_create(name=name.strip())
        return tag, BookmarkTags.get_or_create(
            tag_id=tag.id,
            bookmark_id=self.id,
        )

    @property
    def tags(self):
        return [b.tag for b in BookmarkTags.find_by(bookmark_id=self.id)]

    def tags_as_json(self):
        return json.dumps([t.to_dict() for t in self.tags])

    def remove_tag(self, tag):
        bookmark_tag = BookmarkTags.find_one_by(tag_id=tag.id, bookmark_id=self.id)
        if bookmark_tag:
            bookmark_tag.delete()


class BookmarkTags(Model):
    table = db.Table('gb_bookmark_tags', metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('tag_id', db.Integer, nullable=False),
        db.Column('bookmark_id', db.Integer, nullable=False),
    )

    @property
    def tag(self):
        return Tag.find_one_by(id=self.tag_id)

    @property
    def bookmark(self):
        return Bookmark.find_one_by(id=self.bookmark_id)


class HttpCache(Model):
    TIMEOUT = 10800
    table = db.Table('gb_http_cache', metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('url', db.Unicode(length=200), nullable=False),
        db.Column('token', db.String(length=200), nullable=False),
        db.Column('content', db.UnicodeText, nullable=False),
        db.Column('headers', db.UnicodeText, nullable=False),
        db.Column('status_code', db.Integer, nullable=False),
        db.Column('updated_at', db.DateTime, default=now)
    )

    def to_cache_dict(self):
        return {
            'url': self.url,
            'response_data': self.content,
            'response_headers': ejson.loads(self.headers or "{}"),
            'cached': True,
            'status_code': self.status_code,
        }

    @classmethod
    def get(cls, key):
        return {}

    @classmethod
    def set(cls, key, value):
        return {}
