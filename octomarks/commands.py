#!/usr/bin/env python
# -*- coding: utf-8; -*-
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


from flask.ext.script import Command


class UpdateUserTags(Command):
    def run(self):
        from octomarks.models import Bookmark
        for b in Bookmark.all():
            print "processing from {0}".format(b.url[19:])
            for tag in b.get_tags():
                print "    Adding tag {0} to user {1}".format(tag['name'], b.user.username)
                b.user.add_tag(tag['name'])


class SyncDB(Command):
    def __init__(self, destructive=False):
        self.destructive = destructive

    def run(self):
        from octomarks.models import db, metadata

        if self.destructive:
            print "Destroying tables under", db.engine
            metadata.drop_all(db.engine)

        print "Creating tables under", db.engine
        metadata.create_all(db.engine)


class Runserver(Command):
    def run(self):
        from octomarks.app import app
        from octomarks import settings

        if settings.DEBUG:
            return app.web.run(debug=True)

        elif settings.PRODUCTION:
            http_server = HTTPServer(WSGIContainer(app.web))
            http_server.listen(settings.PORT)
            IOLoop.instance().start()


def init_command_manager(manager):
    manager.add_command('renewdb', SyncDB(destructive=True))
    manager.add_command('syncdb', SyncDB())
    manager.add_command('update-user-tags', UpdateUserTags())
    manager.add_command('run', Runserver())
    return manager
