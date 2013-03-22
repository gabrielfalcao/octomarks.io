#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    Blueprint, request, session, render_template, redirect, url_for, g, flash
)

from merchants.utils import requires_login

mod = Blueprint('views', __name__)


COOKIE_NAME = 'login-malandro'


@mod.before_request
def load_current_user():
    from merchants.models import Merchant
    g.user = Merchant.query.filter_by(email=session[COOKIE_NAME]).first() \
        if COOKIE_NAME in session else None


@mod.route('/')
def index():
    next_page = COOKIE_NAME in session and '.dashboard' or '.join'
    return redirect(url_for(next_page))


@mod.route('/logout')
def logout():
    if COOKIE_NAME in session:
        del session[COOKIE_NAME]
    g.user = None
    return redirect(request.referrer or url_for('.index'))


@mod.route('/join')
def join():
    return render_template('teaser.html')


@mod.route('/signup', methods=('GET', 'POST'))
def signup():
    from merchants.forms import SignupForm
    from merchants.models import Merchant
    from merchants.app import app

    form = SignupForm(csrf_enabled=False)
    if form.validate_on_submit():
        inst = Merchant(
            business_id=form.business_id.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
        )
        app.db.session.add(inst)
        app.db.session.commit()

        session[COOKIE_NAME] = form.email.data
        return redirect(url_for('.dashboard'))
    if form.errors:
        flash(
            'We found some things that need to fix before '
            'creating your profile')
    return render_template('signup.html', form=form)


@mod.route('/preview')
def preview():
    return render_template('preview.html')


@mod.route('/purchase')
def purchase():
    return render_template('purchase.html')


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
