import os

from flask import Flask
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

from merchants.assets import AssetsManager
from merchants.commands import init_command_manager
from merchants import views


__all__ = 'app',


class App(object):
    """Manage the main web app and all its subcomponents.

    By subcomponents I mean the database access, the command interface,
    the static assets, etc.
    """

    def __init__(self, settings_path='merchants.settings'):
        self.web = Flask(__name__)

        # Loading our settings
        self.web.config.from_object(settings_path)

        # Loading our JS/CSS
        self.assets = AssetsManager(self.web)
        self.assets.create_bundles()

        # Setting up our commands
        self.commands = init_command_manager(Manager(self.web))
        self.assets.create_assets_command(self.commands)

        # Setting up our database component
        self.db = SQLAlchemy(self.web)

        # Time to register our blueprints
        self.web.register_blueprint(views.mod)

    @staticmethod
    def from_env():
        """Return an instance of `App` fed with settings from the env.
        """
        smodule = os.environ.get(
            'MERCHANTS_SETTINGS_MODULE',
            'merchants.settings'
        )
        return App(smodule)


app = App.from_env()
