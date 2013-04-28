# -*- coding: utf-8 -*-
import re
import ejson as json
import ejson.serializers
import hashlib
from datetime import datetime
# from werkzeug import generate_password_hash, check_password_hash
import logging

logger = logging.getLogger('octomarks.models')

from octomarks.db import db, metadata, Model
from octomarks.core import RepoInfo
from octomarks import settings


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
        db.Column('default_theme_name', db.String(255), default='tango',
                  nullable=False),
        db.Column('updated_at', db.DateTime, default=now),
    )

    def initialize(self):
        from octomarks.api import GithubUser
        sha = hashlib.sha1()
        sha.update("octomarks:")
        sha.update(self.username)
        self.gb_token = sha.hexdigest()
        self.api = GithubUser.from_token(self.github_token)

    def __repr__(self):
        return '<User %r, token=%r>' % (self.username, self.gb_token)

    def save_bookmark(self, uri):
        # TODO: take project, languages and all the other data that
        # will be fetched by the view, so you can have more
        # information.
        info = RepoInfo(uri.strip())
        if info:
            bk = Bookmark.get_or_create(user_id=self.id, url=info.remount())
            tags = self.api.endpoint.retrieve('/repos/{0}/{1}/languages'.format(info.owner, info.project))
            tags = map(bk.add_tag, tags)
            return bk

    def get_bookmarks(self):
        return Bookmark.find_by(user_id=self.id)

    def save_repo_as_bookmark(self, repo):
        return self.save_bookmark(repo['html_url'])

    def import_starred_as_bookmarks(self):
        repos = self.api.get_starred(self.username)
        try:
            return map(self.save_repo_as_bookmark, repos)
        except Exception:
            logger.exception("Could not get starred repos for %s:\n%s", self.username, repr(repos))

    def change_theme_to(self, name):
        self.default_theme_name = name
        self.save()

    def get_theme(self):
        name = self.default_theme_name
        return {
            'name': name,
            'url': settings.absurl('static', 'themes', '{0}.css'.format(name))
        }

    @classmethod
    def create_from_github_user(cls, data):
        login = data.get('login')
        instance = cls.create(
            username=login,
            github_id=data.get('id'),
            gravatar_id=data.get('gravatar_id'),
            email=data.get('email', "{0}@octomarks.com".format(login)),
            github_token=data.get('github_token')
        )
        logger.info("user %d created: %s", instance.id, instance.email)
        return instance

    @classmethod
    def get_or_create_from_github_user(cls, data):
        instance = cls.find_one_by(username=data['login'])

        if not instance:
            instance = cls.create_from_github_user(data)
            instance.import_starred_as_bookmarks()
        else:
            instance.github_token = data.get('github_token')
            instance.email = data.get('email', instance.email)
            instance.save()

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
        db.Column('token', db.String(length=200), nullable=True),
        db.Column('content', db.UnicodeText, nullable=True),
        db.Column('headers', db.UnicodeText, nullable=True),
        db.Column('status_code', db.Integer, nullable=True),
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


class Ranking(object):
    @classmethod
    def get_top_projects(cls, limit=5):
        field = Bookmark.table.c
        q = (db.select([
            field.url,
            db.func.count('user_id')
        ])
            .group_by(field.url)
            .order_by(db.desc(db.func.count('user_id')))
            .limit(limit))

        conn = Bookmark.get_connection()
        res = conn.execute(q)

        return [cls.repository_with_data(url, dict(total_bookmarks=count))
                for url, count in res.fetchall()]

    @classmethod
    def get_top_users(cls, limit=5):
        field = Bookmark.table.c
        q = (db.select([
            field.user_id,
            db.func.count('url')
        ])
            .group_by(field.user_id)
            .order_by(db.desc(db.func.count('url')))
            .limit(limit))

        conn = Bookmark.get_connection()
        res = conn.execute(q)

        return [cls.user_with_data(user_id, dict(total_bookmarks=count))
                for user_id, count in res.fetchall()]

    @classmethod
    def repository_with_data(cls, url, data=None):
        from octomarks.api import GithubRepository, GithubEndpoint

        data = data or {}

        repo = GithubRepository(GithubEndpoint(cls.get_most_recent_token()))
        data['meta'] = info = RepoInfo(url)
        data['info'] = repo.get(owner=info.owner, project=info.project)

        return data

    @classmethod
    def user_with_data(cls, user_id, data=None):
        data = data or {}

        data['info'] = User.find_one_by(id=user_id).to_dict()

        return data

    @classmethod
    def get_most_recent_token(cls):
        field = User.table.c
        q = (db.select([field.github_token])
            .order_by(db.desc(field.updated_at))
            .limit(1))

        conn = Bookmark.get_connection()
        res = conn.execute(q)
        if res.returns_rows:
            return res.fetchone()[0]

        return 'NONE'
