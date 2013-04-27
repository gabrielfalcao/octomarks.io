#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import httpretty
from mock import Mock
from sure import scenario

from octomarks.app import app
from octomarks.models import User, db, metadata, Bookmark

HTTPRETY_METHODS = [
    httpretty.GET,
    httpretty.POST,
    httpretty.PUT,
    httpretty.DELETE,
]


def prepare(context):
    httpretty.register_uri(
        httpretty.GET,
        re.compile('github.com/repos/\w+/\w+/languages'),
        body='[]',
        content_type='application/json')

    conn = db.engine.connect()
    metadata.drop_all(db.engine)
    metadata.create_all(db.engine)
    conn.execute(User.table.delete())
    context.app = app.web.test_client()

    for METHOD in HTTPRETY_METHODS:
        body = json.dumps(
            {
                'access_token': 'httpretty token',
                'functional testing': True
            }
        )
        httpretty.register_uri(METHOD, re.compile("(.*)"), body)

    class FakeUser(User):
        api = Mock()

        def initialize(self):
            self.gb_token = 'abcd' * 10

    context.User = FakeUser

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


def create_3_users(context):
    for i in range(1, 4):
        data = {}
        data['username'] = "login{0}".format(i)
        data['github_id'] = 42 + i
        data['email'] = 'user{0}@gmail.com'.format(i)
        data['github_token'] = str(i) * 10
        data['gravatar_id'] = str(i) * 10
        setattr(context, 'user{0}'.format(i),
                User.create(**data))


def create_bookmark(context):
    context.bookmark = Bookmark.create(
        url="http://github.com/clarete/forbidden_fruit",
        user_id=1,
    )


user_test = scenario([prepare, create_user])
multi_user_test = scenario([prepare, create_3_users])
bookmark_test = scenario([prepare, create_bookmark])

user_bookmark_test = scenario([prepare, create_user, create_bookmark])
