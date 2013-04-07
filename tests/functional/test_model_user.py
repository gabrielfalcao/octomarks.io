#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import db_test
from gbookmarks.models import User


@db_test
def test_user_signup(context):
    ("User.create_from_github_user(dict) should create a "
     "user in the database")
    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "type": "User",
        "github_token": 'toktok',
    }

    created = User.create_from_github_user(data)

    created.should.have.property('id').being.equal(1)
    created.should.have.property('username').being.equal("octocat")
    created.should.have.property('github_id').being.equal(42)
    created.should.have.property('github_token').being.equal('toktok')
    created.should.have.property('gravatar_id').being.equal('somehexcode')
    created.should.have.property('email').being.equal('octocat@github.com')
    created.should.have.property('gb_token').being.length_of(40)


@db_test
def test_user_signup_get_or_create_if_already_exists(context):
    ("User.get_or_create_from_github_user(dict) should get"
     "user from the database if already exists")

    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "type": "User",
        "github_token": '123',
    }

    created = User.create_from_github_user(data)
    got = User.get_or_create_from_github_user(data)

    got.should.equal(created)


@db_test
def test_user_signup_get_or_create_doesnt_exist(context):
    ("User.get_or_create_from_github_user(dict) should get"
     "user from the database if it does not exist yet")

    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "github_token": "toktok",
        "type": "User"
    }

    created = User.get_or_create_from_github_user(data)

    created.should.have.property('id').being.equal(1)
    created.should.have.property('username').being.equal("octocat")
    created.should.have.property('github_id').being.equal(42)
    created.should.have.property('github_token').being.equal('toktok')
    created.should.have.property('gravatar_id').being.equal('somehexcode')
    created.should.have.property('email').being.equal('octocat@github.com')
    created.should.have.property('gb_token').being.length_of(40)


@db_test
def test_find_one_by(context):
    ("User.find_one_by(**kwargs) should fetch user from the database")

    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "github_token": "toktok",
        "type": "User"
    }

    original_user = User.create_from_github_user(data)

    User.find_one_by(id=1).should.be.equal(original_user)
    User.find_one_by(username='octocat').should.be.equal(original_user)


@db_test
def test_find_by(context):
    ("User.find_by(**kwargs) should fetch a list of users from the database")

    data1 = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode2",
        "email": "octocat@github.com",
        "github_token": "toktok",
        "type": "User"
    }

    data2 = {
        "login": "octopussy",
        "id": 88,
        "gravatar_id": "somehexcode1",
        "email": "octopussy@github.com",
        "github_token": "toktok",
        "type": "User"
    }

    original_user1 = User.create_from_github_user(data1)
    original_user2 = User.create_from_github_user(data2)

    User.find_by(github_token='toktok').should.be.equal([
        original_user1,
        original_user2
    ])
