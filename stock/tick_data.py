__author__ = 'kittaaron'
# 分配预案

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig
import sys

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def get_today_ticks(code):
    # df = ts.get_tick_data('000576', date='2017-08-12')
    # df = ts.get_tick_data('300266', date='2014-01-09')
    # code = '300266'
    df = ts.get_today_ticks(code)
    bamount = samount = 0
    smallbamount = smallsamount = 0
    logging.info(df)

    for index, serie in df.iterrows():
        type = serie.type
        volume = serie.volume
        amount = serie.amount

        if serie.type == '买盘':
            bamount += serie.amount

        if serie.type == '卖盘':
            samount += serie.amount
    logging.info("买盘: %s 卖盘: %s net: %s ", bamount, samount, (bamount - samount))
    # df.to_sql('tick_data', engine, if_exists='replace', index=False, index_label='code')


def get_ticks(code, date):
    df = ts.get_tick_data(code, date=date)
    bamount = samount = 0

    for index, serie in df.iterrows():
        type = serie.type
        volume = serie.volume
        amount = serie.amount

        if type == '买盘':
            bamount += amount

        if type == '卖盘':
            samount += amount
    logging.info("买盘(元): %s 卖盘: %s net: %s ", bamount, samount, (bamount - samount))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        code = sys.argv[1]
        get_today_ticks(code)
    if len(sys.argv) == 3:
        code = sys.argv[1]
        date = sys.argv[2]
        get_ticks(code, date)
