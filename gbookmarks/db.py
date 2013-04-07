# -*- coding: utf-8 -*-

from flask import config
from gbookmarks.app import app


db = app.db

metadata = db.MetaData()


class ORM(type):
    orm = config.Config(None)

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'table'):
            return

        cls.__columns__ = {c.name: c.type.python_type
                           for c in cls.table.columns}

        super(ORM, cls).__init__(name, bases, attrs)

        if name not in ('ORM', 'Model'):
            ORM.orm[name] = cls


class Model(object):
    __metaclass__ = ORM

    def __init__(self, **data):
        Model = self.__class__
        module = Model.__module__
        name = Model.__name__
        columns = self.__columns__.keys()
        self.__data__ = data

        for k, v in data.iteritems():
            if k not in self.__columns__:
                msg = "{0} is not a valid column name for the model {1}.{2} ({3})"
                raise InvalidColumnName(msg.format(k, name, module, columns))

            setattr(self, k, v)

        self.initialize()

    def __setattr__(self, attr, value):
        data_type = self.__columns__.get(attr, None)
        if data_type:
            self.__data__[attr] = data_type(value)

        return super(Model, self).__setattr__(attr, value)

    def __getattr__(self, attr):
        if attr.startswith('__'):
            return super(Model, self).__getattribute__(attr)

        if attr in self.__columns__:
            return self.__data__[attr]

        return super(Model, self).__getattribute__(attr)

    def to_dict(self):
        return self.__data__.copy()

    @property
    def is_persisted(self):
        return 'id' in self.__data__

    @property
    def __conn__(self):
        return db.engine.connect()

    def save(self):
        res = self.__conn__.execute(self.table.insert().values(**self.to_dict()))
        self.__data__['id'] = res.lastrowid
        self.__data__.update(res.last_inserted_params())
        return self

    def get(self, name, fallback=None):
        return self.__data__.get(name, fallback)

    def initialize(self):
        pass


class InvalidColumnName(Exception):
    pass


models = ORM.orm
