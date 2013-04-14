#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import db_test
from freezegun import freeze_time
from httpretty import HTTPretty, httprettified

from gbookmarks.api import GithubEndpoint
from gbookmarks.models import HttpCache


@db_test
@httprettified
@freeze_time("2013-04-14 00:00:00")
def test_get_from_cache(context):
    ("Retrieving a url with cache")
    HTTPretty.register_uri(HTTPretty.GET, "https://api.github.com/user",
                           body='{"login": "gabrielfalcao"}',
                           content_type="application/json")

    api = GithubEndpoint('SOMETOKEN', cache=True)
    data = api.retrieve("/user")
    data.should.have.key("login").being.equal("gabrielfalcao")

    cached = HttpCache.find_one_by(url="https://api.github.com/user")
    # cached.should_not.be.none
