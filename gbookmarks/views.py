#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import (
    Blueprint, request, session, render_template, redirect, g, flash, Response
)


from gbookmarks import settings
from gbookmarks.api import GithubUser
from gbookmarks.handy.decorators import requires_login
from flaskext.github import GithubAuth


github = GithubAuth(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    session_key='user_id'
)

mod = Blueprint('views', __name__)


def json_response(data):
    return Response(json.dumps(data, indent=4), mimetype="text/json")


@mod.before_request
def prepare_auth():
    g.user = None
    g.github = github


@mod.context_processor
def inject_basics():
    return dict(user=g.user, settings=settings)


@github.access_token_getter
def get_github_token(token=None):
    return session.get('github_token')


@mod.before_request
def prepare_user():
    from gbookmarks.models import User
    if 'github_user_data' in session:
        g.user = User.get_or_create_from_github_user(session['github_user_data'])


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
    session['github_user_data'] = github_user_data

    return redirect(next_url)


@mod.route('/save/<token>')
@requires_login
def save_bookmark(token):
    uri = request.args.get('uri')
    return render_template('saved.html', uri=uri)


@mod.route('/bookmarklet/gb_<token>.js')
@requires_login
def serve_bookmarklet(token):
    return render_template('bookmarklet.js', github_user_data=session['github_user_data'])


@mod.route('/login')
def login():
    cb = settings.absurl('.callback')
    return github.authorize(callback_url=cb)


@mod.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')


@mod.route("/")
@requires_login
def index():
    return render_template('index.html')
