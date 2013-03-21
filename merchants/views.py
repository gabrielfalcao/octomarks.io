from flask import Blueprint, render_template

mod = Blueprint('views', __name__)


@mod.route('/')
def index():
    return render_template('index.html')


@mod.route('/dashboard/')
def dashboard():
    return render_template('dashboard/main.html')


@mod.route('/dashboard/competitors/')
def dashboard_competitors():
    return render_template('dashboard/competitors.html')


# deprecated stuff, maybe

@mod.route('/dashboard-old/')
def dashboard_old():
    return render_template('dashboard/old.html')
