__author__ = 'kittaaron'
# 限售解禁

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def get_xsjj():
    df = ts.xsg_data(year=2018, month=7)
    df.to_sql('xsjj', engine, if_exists='append', index=False, index_label='code')


if __name__ == '__main__':
    get_xsjj()