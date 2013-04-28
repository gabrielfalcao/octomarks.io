#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httpretty
from .base import user_test
from octomarks.testing import Client


@httpretty.activate
@user_test
def test_anonymous_index(context):
    ("An anonymous user that goes to / should be redirected to the explore")

    http = Client()

    response = http.get("/")
    (response
     .should
     .have
     .property("location")
     .being
     .equal("http://localhost/explore"))


@httpretty.activate
@user_test
def test_authenticated_index(context):
    ("An authenticated user that goes to / should be redirected to his page")

    http = Client()
    with http.session_transaction() as session:
        session['github_user_data'] = {
            'login': 'octocat',
        }

    response = http.get("/")
    (response
     .should
     .have
     .property("location")
     .being
     .equal("http://localhost/octocat"))
