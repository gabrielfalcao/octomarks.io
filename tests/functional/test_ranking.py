#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httpretty
from .base import db_test, multi_user_test
from octomarks.core import RepoInfo
from octomarks.models import Ranking


@httpretty.activate
@db_test
def test_top_projects(context):
    ("Ranking.get_top_projects should return the top 5 projects")

    context.bookmark_n_times(5, "github.com/gabrielfalcao/HTTPretty")
    context.bookmark_n_times(4, "github.com/gabrielfalcao/sure")
    context.bookmark_n_times(3, "github.com/clarete/forbiddenfruit")
    context.bookmark_n_times(2, "github.com/spulec/freezegun")
    context.bookmark_n_times(1, "github.com/gabrielfalcao/lettuce")
    context.bookmark_n_times(1, "github.com/gabrielfalcao/couleur")
    context.bookmark_n_times(1, "github.com/gabrielfalcao/markment")

    projects = Ranking.get_top_projects()

    projects.should.have.length_of(5)

    first = projects[0]

    first.should.have.key('total_bookmarks').being.equal(5)
    first.should.have.key('info').being.a(dict)

    first['info'].should.have.key('name').being.equal("HTTPretty")
    first['info'].should.have.key('owner').being.a(dict)
    first['info']['owner'].should.have.key('login').being.equal('gabrielfalcao')
    first.should.have.key('meta').being.a(RepoInfo)


@httpretty.activate
@multi_user_test(6)
def test_top_users(context):
    ("Ranking.get_top_users should return the top 5 users")

    context.add_n_bookmarks(5, context.user1)
    context.add_n_bookmarks(4, context.user2)
    context.add_n_bookmarks(3, context.user3)
    context.add_n_bookmarks(2, context.user4)
    context.add_n_bookmarks(1, context.user5)

    users = Ranking.get_top_users()

    users.should.have.length_of(5)

    first = users[0]

    first.should.have.key('total_bookmarks').being.equal(5)
    first.should.have.key('info').being.a(dict)
    first['info'].should.equal(context.user1.to_dict())
