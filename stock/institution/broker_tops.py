__author__ = 'kittaaron'
# 营业部上榜统计

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


def get_broker_tops():
    df = ts.broker_tops()
    df.to_sql('broker_tops', engine, if_exists='append', index=False, index_label='code')


if __name__ == '__main__':
    get_broker_tops()