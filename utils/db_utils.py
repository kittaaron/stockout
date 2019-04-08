# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config.dbconfig as dbconfig
import config.logginconfig
import logging

engine = create_engine(dbconfig.getConfig('database', 'connURL'), pool_size=20, pool_recycle=3600)
Session = sessionmaker(bind=engine)
#session = Session()


def getSession():
    return Session()