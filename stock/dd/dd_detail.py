__author__ = 'kittaaron'
# 某一支股票的大单交易明细

import tushare as ts
import sys
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from config import dbconfig
import datetime
from model.StockInfo import StockInfo
from model.DaDan import DaDan
from model.DaDanSts import DaDanSts
from model.StockInfo import StockInfo
from model.HistData import HistData

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def dd_detail(code):
    end_date = datetime.date.today()
    total_delta = datetime.timedelta(days=0)
    start_date = end_date - total_delta
    date_str = start_date.strftime('%Y-%m-%d')
    logging.info("get dd %s %s", code, date_str)
    df = ts.get_sina_dd(code, date_str)
    if df is None:
        logging.info("%s %s get none", code, date_str)
        return

    bvolume = svolume = 0
    for index, serie in df.iterrows():
        logging.info("%s %s %s %s %s %s %s", code, serie['name'], serie.time, serie.price, serie.preprice, serie.volume, serie.type)
        if serie.type == '买盘':
            bvolume += serie.volume
        if serie.type == '卖盘':
            svolume += serie.volume
    logging.info("买盘: %s, 卖盘: %s, 净值: %s", bvolume, svolume, (bvolume - svolume))


if __name__ == '__main__':
    code = sys.argv[1]
    dd_detail(code)