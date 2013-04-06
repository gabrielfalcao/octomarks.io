#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gbookmarks.db import models
from gbookmarks.models import User, Tag


def test_can_find_models():
    ("db.models should be hold all the declared models")

    models.should.have.key('User').being.equal(User)
    models.should.have.key('Tag').being.equal(Tag)
