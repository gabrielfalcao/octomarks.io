#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import (
    Blueprint, request, session, render_template, redirect, url_for, g, flash
)

from gbookmarks.api import GithubUser
from gbookmarks import settings


from flask_oauth import OAuth


oauth = OAuth()

github = oauth.remote_app('github',
                          base_url='https://api.github.com/',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    request_token_url=None,
    consumer_key=settings.GITHUB_CONSUMER_KEY,
                          consumer_secret=settings.GITHUB_ACCESS_TOKEN_URL)


mod = Blueprint('views', __name__)


@mod.before_request
def prepare_auth():
    g.user = None
    g.github = github


# @mod.teardown_request
# def teardown_request(exception):
#     del g.github
#     del g.user


@mod.context_processor
def inject_basics():
    return dict(user=g.user, settings=settings)


@github.tokengetter
def get_github_token(token=None):
    return session.get('github_token')


@mod.before_request
def prepare_user():
    if 'gbuser' in session:
        g.user = GithubUser(session['gbuser'], session['github_token'])


@mod.route('/.callback')
@github.authorized_handler
def github_callback(resp):
    next_url = request.args.get('next') or '/'
    if resp is None:
        print (u'You denied the request to sign in.')
        return redirect(next_url)

    error = resp.get('error')

    if error:
        flash(error)
        print error
        return json.dumps(error)

    token = resp['access_token']
    session['github_token'] = token

    session['gbuser'] = g.user = GithubUser.from_token(token)
    return redirect(next_url)


@mod.route('/login')
def login():
    return github.authorize(callback=settings.absurl('.callback'))


@mod.route("/")
def index():
    if not session.get('gbuser'):
        url = settings.absurl('login')
        return redirect(url)

    repositories = g.user.get_starred_repositories()
    return render_template('index.html', repositories=repositories, page='starred')


@mod.route("/watching")
def watching():
    if not session.get('gbuser'):
        return redirect(settings.absurl('login'))

    repositories = g.user.get_watched_repositories()

    return render_template('index.html', repositories=repositories, page='watched')
