__author__ = 'kittaaron'
# 分配预案

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def get_fpya():
    df = ts.profit_data(top=3500)
    df.to_sql('fpya', engine, if_exists='replace', index=False, index_label='code')


if __name__ == '__main__':
    get_fpya()