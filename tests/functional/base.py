#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sure import scenario
from octomarks.models import User, db, metadata, Bookmark


def prepare(context):
    conn = db.engine.connect()
    metadata.drop_all(db.engine)
    metadata.create_all(db.engine)
    conn.execute(User.table.delete())

db_test = scenario(prepare)


def create_user(context):
    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "type": "User",
        "github_token": 'toktok',
    }
    context.user = User.create_from_github_user(data)


def create_3_users(context):
    for i in range(1, 4):
        data = {}
        data['login'] = "login{0}".format(i)
        data['id'] = 42 + i
        data['email'] = 'user{0}@gmail.com'.format(i)
        data['github_token'] = str(i) * 10
        data['gravatar_id'] = str(i) * 10
        setattr(context, 'user{0}'.format(i),
                User.create_from_github_user(data))


def create_bookmark(context):
    context.bookmark = Bookmark.create(
        url="http://github.com/clarete/forbidden_fruit",
        user_id=1,
    )


user_test = scenario([prepare, create_user])
multi_user_test = scenario([prepare, create_3_users])
bookmark_test = scenario([prepare, create_bookmark])
