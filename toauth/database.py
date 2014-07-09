#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


db_url = 'sqlite:///sqlite.db'
engine = create_engine(db_url)
DB = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


def syncdb():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
