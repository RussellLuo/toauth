#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Table, select
from sqlalchemy.types import Integer, PickleType

from .database import Base


# database table for session
session = Table('auth_session', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('data', PickleType),
)


class Session(object):
    """Session engine."""

    def __init__(self, db, _id):
        self.db = db
        self.load(_id)

    # def __getattr__(self, name):
    #     return getattr(self.data, name)

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def pop(self, key, *args):
        self.data.pop(key, *args)

    def update(self, data):
        self.data.update(data)

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()

    def clear(self):
        self.data.clear()

    def load(self, _id):
        result = None
        try:
            if _id:
                sql = (select([session.c.id, session.c.data])
                             .where(session.c.id == int(_id)))
                result = self.db.execute(sql).first()
        except ValueError:
            pass

        if result:
            self.id = _id
            self.data = result['data']
        else:
            sql = session.insert().values(data={})
            self.id = str(self.db.execute(sql).inserted_primary_key[0])
            self.data = {}

    def save(self):
        sql = (session.update()
                      .where(session.c.id == self.id)
                      .values(data=self.data))
        self.db.execute(sql)
        self.db.commit()

    def delete(self):
        pass
