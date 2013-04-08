#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sure import scenario
from gbookmarks.models import User, db, metadata, Bookmark


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


def create_bookmark(context):
    context.bookmark = Bookmark.create(
        url="http://github.com/clarete/forbidden_fruit",
        user_id=1,
    )


user_test = scenario([prepare, create_user])
bookmark_test = scenario([prepare, create_bookmark])
