#!/usr/bin/env python
# -*- coding: utf-8; -*-
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


from flask.ext.script import Command


class SyncDB(Command):
    def run(self):
        from gbookmarks.models import db, metadata

        metadata.drop_all(db.engine)
        metadata.create_all(db.engine)


class Runserver(Command):
    def run(self):
        from gbookmarks.app import app
        from gbookmarks import settings

        if settings.DEBUG:
            return app.web.run(debug=settings.DEBUG)

        elif settings.PRODUCTION:
            http_server = HTTPServer(WSGIContainer(app.web))
            http_server.listen(settings.PORT)
            IOLoop.instance().start()


def init_command_manager(manager):
    manager.add_command('syncdb', SyncDB())
    manager.add_command('run', Runserver())
    return manager
