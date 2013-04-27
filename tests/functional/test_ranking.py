#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httpretty
from .base import multi_user_test
from octomarks.models import Bookmark


@httpretty.activate
@multi_user_test
def test_delete_bookmark(context):
    ("Bookmark#delete should delete an existing bookmark")

    context.user1.save_bookmark(
        "http://github.com/gabrielfalcao/HTTPretty")
    context.user2.save_bookmark(
        "http://github.com/gabrielfalcao/HTTPretty")
    context.user3.save_bookmark(
        "http://github.com/gabrielfalcao/HTTPretty")

    context.user2.save_bookmark(
        "http://github.com/gabrielfalcao/lettuce")

    context.user3.save_bookmark(
        "http://github.com/gabrielfalcao/sure")

    bookmarks = Bookmark.get_most_bookmarked()

    bookmarks.should.have.length_of(3)

    bookmarks[0][0].remount().should.equal(
        "http://github.com/gabrielfalcao/HTTPretty")
    bookmarks[0][1].should.equal(3)

    bookmarks[1][0].remount().should.equal(
        "http://github.com/gabrielfalcao/lettuce")
    bookmarks[1][1].should.equal(1)

    bookmarks[2][0].remount().should.equal(
        "http://github.com/gabrielfalcao/sure")
    bookmarks[2][1].should.equal(1)
