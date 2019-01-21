# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config.dbconfig as dbconfig

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def save(data, autocommit=True):
    try:
        session.add(data)
        if autocommit:
            session.commit()
    except Exception as e:
        session.close()


def save_list(datas, autocommit=True):
    try:
        session.add_all(datas)
        if autocommit:
            session.commit()
    except Exception as e:
        session.close()