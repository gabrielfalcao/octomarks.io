#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import (
    Blueprint, request, session, render_template, redirect, g, flash
)


from gbookmarks import settings
from gbookmarks.api import GithubUser

from flaskext.github import GithubAuth


github = GithubAuth(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    session_key='user_id'
)

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


@github.access_token_getter
def get_github_token(token=None):
    return session.get('github_token')


@mod.before_request
def prepare_user():
    if 'gbuser' in session:
        g.user = GithubUser(session['gbuser'], session['github_token'])


@mod.route('/.callback')
@github.authorized_handler
def github_callback(resp):
    from gbookmarks.models import User
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

    github_user_data = GithubUser.from_token(token)

    github_user_data['github_token'] = token
    g.user = User.get_or_create_from_github_user(github_user_data)
    session['gbuser'] = github_user_data

    print "." * 100
    print "user created", g.user.to_dict()
    print "." * 100
    return redirect(next_url)


@mod.route('/login')
def login():
    cb = settings.absurl('.callback')
    return github.authorize(callback_url=cb)


@mod.route('/logout')
def logout():
    session.clear()
    del g.user
    return render_template('logout.html')


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
