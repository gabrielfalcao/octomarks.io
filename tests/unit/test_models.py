#!/usr/bin/env python
# -*- coding: utf-8 -*-

from octomarks.db import models
from octomarks.models import User, Tag, Bookmark


def test_can_find_models():
    ("db.models should be hold all the declared models")

    models.should.have.key('User').being.equal(User)
    models.should.have.key('Tag').being.equal(Tag)
    models.should.have.key('Bookmark').being.equal(Bookmark)
