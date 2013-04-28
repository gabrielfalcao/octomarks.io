# -*- coding: utf-8 -*-
import re
import json
import sure
import httpretty
from lxml import html as lhtml
from lettuce import world, before, after
from octomarks.testing import Client
from octomarks.models import (
    db,
    metadata,
    User,
    Bookmark,
    Tag,
    BookmarkTags,
    HttpCache,
)

HTTPRETY_METHODS = [
    httpretty.GET,
    httpretty.POST,
    httpretty.PUT,
    httpretty.DELETE,
]


@before.all
def enable_httpretty(*args):
    httpretty.enable()

    httpretty.register_uri(
        httpretty.GET,
        re.compile('github.com/repos/\w+/\w+/languages'),
        body='[]',
        content_type='application/json')

    def GithubRepositoryStub(owner, name):
        return json.dumps(dict(name=name, owner=dict(name=owner)))

    def repository_callback(method, uri, headers):
        return 200, {'server': 'Github'}, GithubRepositoryStub(*uri.strip("/").split("/")[-2:])

    httpretty.register_uri(
        httpretty.GET,
        re.compile('github.com/repos/([^/]+)/([^/]+)/?$'),
        body=repository_callback)


@before.all
def export_models(*args):
    world.User = User
    world.BookmarkTags = BookmarkTags
    world.Bookmark = Bookmark
    world.Tag = Tag
    world.HttpCache = HttpCache


@before.each_scenario
def prepare_db(scenario):
    metadata.drop_all(db.engine)
    metadata.create_all(db.engine)


@after.each_scenario
def cleanup_db(scenario):
    conn = db.engine.connect()
    conn.execute(User.table.delete())
    conn.execute(Bookmark.table.delete())
    conn.execute(Tag.table.delete())
    conn.execute(HttpCache.table.delete())
    conn.execute(BookmarkTags.table.delete())


@world.absorb
def web_client(login=None):
    http = Client()

    if login:
        with http.session_transaction() as session:
            session['github_user_data'] = {
                'login': login,
            }

    return http


@world.absorb
def get_dom(html):
    return lhtml.fromstring(html)

sure
