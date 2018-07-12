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
    df = ts.get_sina_dd(code, date_str)
    logging.info(df)


if __name__ == '__main__':
    code = sys.argv[1]
    dd_detail(code)