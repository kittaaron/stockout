__author__ = 'kittaaron'
# 业绩预告

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def get_yjyg():
    df = ts.forecast_data(2018, 3)
    df.to_sql('yjyg', engine, if_exists='replace', index=False, index_label='code')


if __name__ == '__main__':
    get_yjyg()