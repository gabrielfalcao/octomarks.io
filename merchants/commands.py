from flask.ext.script import Command


class SyncDB(Command):
    def run(self):
        from merchants import models
        from merchants.app import app
        app.db.create_all()


def init_command_manager(manager):
    manager.add_command('syncdb', SyncDB())
    return manager
