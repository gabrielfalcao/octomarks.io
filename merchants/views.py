#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect

mod = Blueprint('views', __name__)


@mod.route('/')
def index():
    # if authenticated, send to dashboard
    return redirect('/join')


@mod.route('/join')
def join_teaser():
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
