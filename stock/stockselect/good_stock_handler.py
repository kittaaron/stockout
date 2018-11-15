__author__ = 'kittaaron'
# 已选大单数据

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig
import datetime
from model.GoodStock import GoodStock
from stock.stockselect import analyzer

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def get_good_stock_codes():
    codes = []
    good_stocks = session.query(GoodStock).filter().all()
    for good_stock in good_stocks:
        codes.append(good_stock.code)
    return codes


def analyse_good_stock(date_str):
    codes = get_good_stock_codes()
    analyzer.analyze_codes_dd(codes, date_str)


if __name__ == '__main__':
    end_date = datetime.date.today()
    total_delta = datetime.timedelta(days=0)
    start_date = end_date - total_delta
    date_str = start_date.strftime('%Y-%m-%d')

    analyse_good_stock(date_str)
