#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    Blueprint, request, session, render_template, redirect, url_for, g
)

from merchants.utils import requires_login

mod = Blueprint('views', __name__)


COOKIE_NAME = 'login-malandro'


@mod.before_request
def load_current_user():
    from merchants.models import Merchant
    g.user = Merchant.query.filter_by(openid=session[COOKIE_NAME]).first() \
        if COOKIE_NAME in session else None


@mod.route('/')
def index():
    next_page = COOKIE_NAME in session and '.dashboard' or '.join'
    return redirect(url_for(next_page))


@mod.route('/logout')
def logout():
    if COOKIE_NAME in session:
        del session[COOKIE_NAME]
    return redirect(request.refferer or url_for('.index'))


@mod.route('/join')
def join():
    return render_template('teaser.html')


@mod.route('/signup')
def signup():
    return render_template('signup.html')


@mod.route('/dashboard/')
@requires_login
def dashboard():
    return render_template('dashboard/main.html')


@mod.route('/dashboard/competitors/')
@requires_login
def track_competitors():
    return render_template('dashboard/competitors.html')


@mod.route('/dashboard/create-campaign/')
@requires_login
def run_deal():
    return render_template('dashboard/run-deal.html')
