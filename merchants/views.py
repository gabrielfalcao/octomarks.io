#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    Blueprint, request, session, render_template, redirect, url_for
)


mod = Blueprint('views', __name__)


COOKIE_NAME = 'login-malandro'


@mod.route('/')
def index():
    next_page = COOKIE_NAME in session and 'dashboard' or 'join'
    return redirect(url_for(next_page))


@mod.route('/logout')
def logout():
    if COOKIE_NAME in session:
        del session[COOKIE_NAME]
    return redirect(request.refferer or url_for('index'))


@mod.route('/join')
def join():
    return render_template('teaser.html')


@mod.route('/signup')
def signup():
    return render_template('signup.html')


@mod.route('/dashboard/')
def dashboard():
    return render_template('dashboard/main.html')


@mod.route('/dashboard/competitors/')
def track_competitors():
    return render_template('dashboard/competitors.html')


@mod.route('/dashboard/create-campaign/')
def run_deal():
    return render_template('dashboard/run-deal.html')
