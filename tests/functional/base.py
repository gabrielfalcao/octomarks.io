#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sure import scenario
from gbookmarks.models import User, db, metadata


def prepare(context):
    conn = db.engine.connect()
    metadata.drop_all(db.engine)
    metadata.create_all(db.engine)
    conn.execute(User.table.delete())

db_test = scenario(prepare)
