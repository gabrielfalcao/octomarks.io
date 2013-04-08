#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import user_test, bookmark_test
from gbookmarks.models import Bookmark


@user_test
def test_delete_bookmark(context):
    ("Bookmark#delete should delete an existing bookmark")

    bookmark = context.user.save_bookmark(
        "http://github.com/gabrielfalcao/HTTPretty")

    bookmark.should.be.within(Bookmark.find_by())

    bookmark.delete()

    bookmark.should_not.be.within(Bookmark.find_by())


@bookmark_test
def test_save_bookmark_with_tags(context):
    ("Bookmark#add_tag should save the tag into the Bookmark")

    t1, rel1 = context.bookmark.add_tag("Domain Specific  Language")
    t1.should.have.property("name").being.equal("domain specific language")
    t1.should.have.property("slug").being.equal("domain-specific-language")

    rel1.should.have.property("tag_id").being.equal(t1.id)
    rel1.should.have.property("bookmark_id").being.equal(context.bookmark.id)
