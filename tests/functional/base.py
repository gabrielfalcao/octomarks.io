#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import httpretty

from mock import Mock
from uuid import uuid4
from sure import scenario, action_for

from octomarks.app import app
from octomarks.models import User, db, metadata, Bookmark

HTTPRETY_METHODS = [
    httpretty.GET,
    httpretty.POST,
    httpretty.PUT,
    httpretty.DELETE,
]


def GithubRepositoryStub(owner, name):
    return json.dumps(dict(name=name, owner=dict(login=owner)))


def setup_httpretty():
    httpretty.register_uri(
        httpretty.GET,
        re.compile('github.com/repos/\w+/\w+/languages'),
        body='[]',
        content_type='application/json')

    def repository_callback(method, uri, headers):
        return 200, {'server': 'Github'}, GithubRepositoryStub(*uri.strip("/").split("/")[-2:])

    httpretty.register_uri(
        httpretty.GET,
        re.compile('github.com/repos/([^/]+)/([^/]+)/?$'),
        body=repository_callback)


def prepare(context):
    setup_httpretty()
    conn = db.engine.connect()
    metadata.drop_all(db.engine)
    metadata.create_all(db.engine)
    conn.execute(User.table.delete())
    context.app = app.web.test_client()

    class FakeUser(User):
        api = Mock()

        def initialize(self):
            self.gb_token = 'abcd' * 10

    context.User = FakeUser

    @action_for(context)
    def bookmark_n_times(times, url):
        for x in range(times):
            code = uuid4().hex
            gid = int("".join(re.findall(r"\d", code))[:8]) + x

            data = {
                "username": code[:10],
                "gravatar_id": code[:20],
                "email": "{0}@github.com".format(code),
                "github_token": code,
                "github_id": gid,
            }
            User.create(**data).save_bookmark(url)

    @action_for(context)
    def add_n_bookmarks(times, user):
        for x in range(times):
            code = uuid4().hex[:10]
            url = "http://github.com/fakeuser/{0}".format(code)
            user.save_bookmark(url)

db_test = scenario([prepare])


def create_user(context):
    data = {
        "username": "octocat",
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "github_token": 'toktok',
        "github_id": '123',
    }
    context.user = User.create(**data)


def create_n_users(number):
    total = number

    def save_users(context):
        context.users = []
        for i in range(1, total + 1):
            data = {}
            data['username'] = "login{0}".format(i)
            data['github_id'] = 42 + i
            data['email'] = 'user{0}@gmail.com'.format(i)
            data['github_token'] = str(i) * 10
            data['gravatar_id'] = str(i) * 10

            user = User.create(**data)

            setattr(context, 'user{0}'.format(i), user)
            context.users.append(user)

    return save_users


def create_bookmark(context):
    context.bookmark = Bookmark.create(
        url="http://github.com/clarete/forbidden_fruit",
        user_id=1,
    )


user_test = scenario([prepare, create_user])
multi_user_test = lambda num=5: scenario([prepare, create_n_users(5)])
bookmark_test = scenario([prepare, create_bookmark])

user_bookmark_test = scenario([prepare, create_user, create_bookmark])
