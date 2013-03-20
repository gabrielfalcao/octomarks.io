from flask import Flask, render_template
from flask.ext.script import Manager

from merchants.assets import AssetsManager

app = Flask(__name__)

# Loading our JS/CSS
assets = AssetsManager(app)
assets.create_bundles()

# Setting up our commands
commands = Manager(app)
assets.create_assets_command(commands)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard/main.html')


@app.route('/dashboard/competitors/')
def dashboard_competitors():
    return render_template('dashboard/competitors.html')
