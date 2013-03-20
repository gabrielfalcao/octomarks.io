from flask import Flask
from flask.ext.script import Manager

from merchants.assets import AssetsManager
from merchants import views


def get_app():
    app = Flask(__name__)

    # Loading our settings
    app.config.from_object('merchants.settings')

    # Loading our JS/CSS
    assets = AssetsManager(app)
    assets.create_bundles()

    # Setting up our commands
    app.commands = Manager(app)
    assets.create_assets_command(app.commands)

    # Time to register our blueprints
    app.register_blueprint(views.mod)

    # We're done, just return the app
    return app
