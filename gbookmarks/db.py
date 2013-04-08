# -*- coding: utf-8 -*-
from functools import partial
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

    def delete(self):
        return self.__conn__.execute(self.table.delete().where(
            self.table.c.id == self.id))

    @classmethod
    def from_result_proxy(cls, proxy, result):
        if not result:
            return None

        data = dict(zip(proxy.keys(), result))
        return cls(**data)

    @classmethod
    def create(cls, **data):
        instance = cls(**data)
        return instance.save()

    @classmethod
    def query_by(cls, **kw):
        conn = db.engine.connect()
        query = cls.table.select()
        for field, value in kw.items():
            query = query.where(getattr(cls.table.c, field) == value)

        proxy = conn.execute(query)
        return proxy

    @classmethod
    def find_one_by(cls, **kw):
        proxy = cls.query_by(**kw)
        return cls.from_result_proxy(proxy, proxy.fetchone())

    @classmethod
    def find_by(cls, **kw):
        proxy = cls.query_by(**kw)

        Users = partial(cls.from_result_proxy, proxy)
        return map(Users, proxy.fetchall())

    @classmethod
    def get_connection(cls):
        return db.engine.connect()

    @property
    def is_persisted(self):
        return 'id' in self.__data__

    @property
    def __conn__(self):
        return self.get_connection()

    def save(self):
        res = self.__conn__.execute(
            self.table.insert().values(**self.to_dict()))
        self.__data__['id'] = res.lastrowid
        self.__data__.update(res.last_inserted_params())
        return self

    def get(self, name, fallback=None):
        return self.__data__.get(name, fallback)

    def initialize(self):
        pass

    def __eq__(self, other):
        return self.__data__ == other.__data__


class InvalidColumnName(Exception):
    pass


class RecordNotFound(Exception):
    pass


models = ORM.orm
