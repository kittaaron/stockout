__author__ = 'kittaaron'
# 获取当时股票结果

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig
import datetime

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def dump_today_all():
    df = ts.get_today_all()
    df.to_sql('today_all', engine, if_exists='append', index=False, index_label='opDate')


if __name__ == '__main__':
    dump_today_all()
