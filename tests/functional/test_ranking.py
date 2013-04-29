#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httpretty
from .base import db_test, multi_user_test, multi_bookmark_test
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


@httpretty.activate
@multi_bookmark_test(5)
def test_top_bookmark_tags(context):
    ("Ranking.get_top_bookmark_tags should return the top 5 tags")

    context.bookmark1.add_tag("Testing")
    context.bookmark1.add_tag("UI")
    context.bookmark1.add_tag("Python")
    context.bookmark1.add_tag("Hacking")

    context.bookmark2.add_tag("Testing")
    context.bookmark2.add_tag("Enterprise")
    context.bookmark2.add_tag("Hacking")

    context.bookmark3.add_tag("Enterprise")
    context.bookmark3.add_tag("Hacking")
    context.bookmark3.add_tag("Ruby")

    context.bookmark4.add_tag("Hacking")
    context.bookmark4.add_tag("GNU")
    context.bookmark5.add_tag("Testing")
    context.bookmark4.add_tag("C")

    context.bookmark5.add_tag("Hacking")
    context.bookmark5.add_tag("Testing")
    context.bookmark5.add_tag("GNU")

    tags = Ranking.get_top_bookmark_tags()
    tags.should.have.length_of(5)

    t1, t2, t3, t4, t5 = tags

    t1.should.have.key('tag').being.a(dict)
    t2.should.have.key('tag').being.a(dict)
    t3.should.have.key('tag').being.a(dict)
    t4.should.have.key('tag').being.a(dict)
    t5.should.have.key('tag').being.a(dict)

    t1['tag'].should.have.key("slug").being.equal("hacking")
    t2['tag'].should.have.key("slug").being.equal("testing")
    t3['tag'].should.have.key("slug").being.equal("enterprise")
    t4['tag'].should.have.key("slug").being.equal("gnu")
    t5['tag'].should.have.key("slug").being.equal("ui")

    t1.should.have.key('total_bookmarks').being.equal(5)
    t2.should.have.key('total_bookmarks').being.equal(3)
    t3.should.have.key('total_bookmarks').being.equal(2)
    t4.should.have.key('total_bookmarks').being.equal(2)
    t5.should.have.key('total_bookmarks').being.equal(1)


@httpretty.activate
@multi_user_test(5)
def test_top_user_tags(context):
    ("Ranking.get_top_user_tags should return the top 5 tags")

    context.user1.add_tag("Testing")
    context.user1.add_tag("UI")
    context.user1.add_tag("Python")
    context.user1.add_tag("Hacking")

    context.user2.add_tag("Testing")
    context.user2.add_tag("Enterprise")
    context.user2.add_tag("Hacking")

    context.user3.add_tag("Enterprise")
    context.user3.add_tag("Hacking")
    context.user3.add_tag("Ruby")

    context.user4.add_tag("Hacking")
    context.user4.add_tag("GNU")
    context.user5.add_tag("Testing")
    context.user4.add_tag("C")

    context.user5.add_tag("Hacking")
    context.user5.add_tag("Testing")
    context.user5.add_tag("GNU")

    tags = Ranking.get_top_user_tags()
    tags.should.have.length_of(5)

    t1, t2, t3, t4, t5 = tags

    t1.should.have.key('tag').being.a(dict)
    t2.should.have.key('tag').being.a(dict)
    t3.should.have.key('tag').being.a(dict)
    t4.should.have.key('tag').being.a(dict)
    t5.should.have.key('tag').being.a(dict)

    t1['tag'].should.have.key("slug").being.equal("hacking")
    t2['tag'].should.have.key("slug").being.equal("testing")
    t3['tag'].should.have.key("slug").being.equal("enterprise")
    t4['tag'].should.have.key("slug").being.equal("gnu")
    t5['tag'].should.have.key("slug").being.equal("ui")

    t1.should.have.key('total_users').being.equal(5)
    t2.should.have.key('total_users').being.equal(3)
    t3.should.have.key('total_users').being.equal(2)
    t4.should.have.key('total_users').being.equal(2)
    t5.should.have.key('total_users').being.equal(1)
