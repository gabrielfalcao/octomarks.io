# -*- coding: utf-8 -*-

from flask import config
from gbookmarks.app import app


db = app.db

metadata = db.MetaData()


class ORM(type):
    orm = config.Config(None)

    def __init__(cls, name, bases, attrs):
        super(ORM, cls).__init__(name, bases, attrs)
        if name not in ('ORM', 'Model'):
            ORM.orm[name] = cls


class Model(object):
    __metaclass__ = ORM

    @classmethod
    def find_by(cls, **kwargs):
        # TODO: implement
        import pdb;pdb.set_trace()

models = ORM.orm
