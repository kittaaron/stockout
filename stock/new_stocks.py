__author__ = 'kittaaron'
# 新股

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def new_stocks():
    df = ts.new_stocks()
    df.to_sql('new_stocks', engine, if_exists='append', index=False, index_label='code')


if __name__ == '__main__':
    new_stocks()