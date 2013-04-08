#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sure import scenario
from gbookmarks.models import User, db, metadata


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


user_test = scenario([prepare, create_user])
