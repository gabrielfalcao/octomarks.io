#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import db_test, user_test
from octomarks.models import User, Bookmark
from octomarks.ui import theme_file


@db_test
def test_user_signup(context):
    ("context.User.create_from_github_user(dict) should create a "
     "user in the database")
    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "type": "User",
        "github_token": 'toktok',
    }

    created = context.User.create_from_github_user(data)

    created.should.have.property('id').being.equal(1)
    created.should.have.property('username').being.equal("octocat")
    created.should.have.property('github_id').being.equal(42)
    created.should.have.property('github_token').being.equal('toktok')
    created.should.have.property('gravatar_id').being.equal('somehexcode')
    created.should.have.property('email').being.equal('octocat@github.com')
    created.should.have.property('gb_token').being.length_of(40)


@db_test
def test_user_signup_get_or_create_if_already_exists(context):
    ("context.User.get_or_create_from_github_user(dict) should get"
     "user from the database if already exists")

    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "type": "User",
        "github_token": '123',
    }

    created = context.User.create_from_github_user(data)
    got = context.User.get_or_create_from_github_user(data)

    got.should.equal(created)


@db_test
def test_user_signup_get_or_create_doesnt_exist(context):
    ("context.User.get_or_create_from_github_user(dict) should get"
     "user from the database if it does not exist yet")
    context.User.api.get_starred.return_value = []
    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "github_token": "toktok",
        "type": "User"
    }

    created = context.User.get_or_create_from_github_user(data)

    created.should.have.property('id').being.equal(1)
    created.should.have.property('username').being.equal("octocat")
    created.should.have.property('github_id').being.equal(42)
    created.should.have.property('github_token').being.equal('toktok')
    created.should.have.property('gravatar_id').being.equal('somehexcode')
    created.should.have.property('email').being.equal('octocat@github.com')
    created.should.have.property('gb_token').being.length_of(40)


@db_test
def test_find_one_by(context):
    ("context.User.find_one_by(**kwargs) should fetch user from the database")

    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "github_token": "toktok",
        "type": "User"
    }

    original_user = context.User.create_from_github_user(data)

    context.User.find_one_by(id=1).should.be.equal(original_user)
    context.User.find_one_by(username='octocat').should.be.equal(original_user)


@db_test
def test_find_one_by_not_exists(context):
    ("context.User.find_one_by(**kwargs) should return None if does not exist")

    context.User.find_one_by(username='octocat').should.be.none


@db_test
def test_find_many_by_not_exists(context):
    ("context.User.find_by(**kwargs) should return an empty list if does not exist")

    context.User.find_by(username='octocat').should.be.empty


@db_test
def test_find_by(context):
    ("context.User.find_by(**kwargs) should fetch a list of users from the database")

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

    context.User.find_by(github_token='toktok').should.be.equal([
        original_user1,
        original_user2
    ])


@user_test
def test_list_bookmark(context):
    ("User#get_bookmarks should return a list of bookmarks")

    b1 = context.user.save_bookmark(
        "http://github.com/gabrielfalcao/sure")

    b2 = context.user.save_bookmark(
        "http://github.com/gabrielfalcao/lettuce")

    context.user.get_bookmarks().should.equal([b1, b2])


@user_test
def test_save_bookmark(context):
    ("User#save_bookmark should take a bookmark link and "
     "return the bookmark")

    bookmark = context.user.save_bookmark(
        "http://github.com/gabrielfalcao/sure")

    bookmark.should.have.property('id').being.equal(1)
    bookmark.should.have.property('url').being.equal(
        "http://github.com/gabrielfalcao/sure")


@user_test
def test_save_bookmark_page(context):
    ("User#save_bookmark should take a bookmark link and "
     "return the bookmark")

    bookmark = context.user.save_bookmark(
        "gabrielfalcao.github.io/sure")

    bookmark.should.have.property('id').being.equal(1)
    bookmark.should.have.property('url').being.equal(
        "http://github.com/gabrielfalcao/sure")


@user_test
def test_save_bookmark_multiple_times(context):
    ("User#save_bookmark with the same uri should save only once")

    bookmark1 = context.user.save_bookmark(
        "http://github.com/gabrielfalcao/sure")

    bookmark2 = context.user.save_bookmark(
        "http://github.com/gabrielfalcao/sure")

    bookmark1.should.equal(bookmark2)

    Bookmark.find_by(user_id=context.user.id).should.have.length_of(1)
    Bookmark.find_by(user_id=context.user.id).should.contain(bookmark1)


@db_test
def test_user_change_theme(context):
    ("Users should be able to change their default theme")

    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "github_token": "toktok",
        "type": "User"
    }

    original_user = context.User.create_from_github_user(data)

    original_user.default_theme_name.should.equal('github')
    original_user.change_theme_to('emacs')

    original_user.default_theme_name.should.equal('emacs')

    fresh_user = User.find_one_by(username='octocat')
    fresh_user.default_theme_name.should.equal('emacs')


@db_test
def test_user_load_theme(context):
    ("Users should be get its css theme")

    data = {
        "login": "octocat",
        "id": 42,
        "gravatar_id": "somehexcode",
        "email": "octocat@github.com",
        "github_token": "toktok",
        "type": "User",
        "default_theme_name": "emacs",
    }

    user = context.User.create_from_github_user(data)

    theme = user.get_theme()

    theme.should.have.key('url').being.equal('http://localhost:5000/static/themes/emacs.css')
    theme.should.have.key('name').being.equal('emacs')
