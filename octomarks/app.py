# -*- coding: utf-8 -*-

import os
import sys
import logging

from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

from logging import getLogger, StreamHandler

from octomarks.assets import AssetsManager
from octomarks.commands import init_command_manager
from octomarks import views


__all__ = 'app',


class App(object):
    """Manage the main web app and all its subcomponents.

    By subcomponents I mean the database access, the command interface,
    the static assets, etc.
    """

    def __init__(self, settings_path='octomarks.settings'):
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

        # Setting logging

        for logger in [self.web.logger, getLogger('sqlalchemy'), getLogger('octomarks.models'), getLogger('octomarks.api')]:
            logger.addHandler(StreamHandler(sys.stderr))
            logger.setLevel(logging.INFO)

        @self.web.errorhandler(500)
        def internal_error(exception):
            self.web.logger.exception(exception)
            return render_template('500.html'), 500

    @classmethod
    def from_env(cls):
        """Return an instance of `App` fed with settings from the env.
        """
        smodule = os.environ.get(
            'OCTOMARKS_SETTINGS_MODULE',
            'octomarks.settings'
        )
        return cls(smodule)


app = App.from_env()
