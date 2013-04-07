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


@db_test
def test_user_signup(context):
    ("User.create_from_github_user(dict) should create a "
     "user in the database")
    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "type": "User"
    }

    created = User.create_from_github_user(data)

    created.should.have.property('id').being.equal(1)
    created.should.have.property('username').being.equal("octocat")
    created.should.have.property('github_id').being.equal(42)
    created.should.have.property('gravatar_id').being.equal('somehexcode')
    created.should.have.property('email').being.equal('octocat@github.com')
    created.should.have.property('gb_token').being.length_of(40)


@db_test
def test_user_signup_get_or_create(context):
    ("User.get_or_create_from_github_user(dict) should get"
     "user from the database")

    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "type": "User"
    }

    created = User.create_from_github_user(data)
    got = User.get_or_create_from_github_user(data)

    got.should.equal(created)
