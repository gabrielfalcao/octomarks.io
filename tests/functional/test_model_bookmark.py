#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import user_test
from gbookmarks.models import Bookmark


@user_test
def test_delete_bookmark(context):
    ("Bookmark#delete should delete an existing bookmark")

    bookmark = context.user.save_bookmark(
        "http://github.com/gabrielfalcao/HTTPretty")

    bookmark.should.be.within(Bookmark.find_by())

    bookmark.delete()

    bookmark.should_not.be.within(Bookmark.find_by())
