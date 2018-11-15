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
from utils.db_utils import *


def get_blue_chip_stock_codes():
    codes = []
    good_stocks = session.query(GoodStock).filter(GoodStock.blue_chip == '蓝筹').all()
    for good_stock in good_stocks:
        codes.append(good_stock.code)
    return codes


def analyse_blue_chip_stock(date_str):
    codes = get_blue_chip_stock_codes()
    analyzer.analyze_codes_dd(codes, date_str)


def analyse_blue_chip_hist(start_date_str, end_date_str):
    codes = get_blue_chip_stock_codes()
    analyzer.analyze_codes_dd(codes, date_str)


if __name__ == '__main__':
    end_date = datetime.date.today()
    total_delta = datetime.timedelta(days=30)
    start_date = end_date - total_delta
    date_str = start_date.strftime('%Y-%m-%d')
    #analyse_blue_chip_stock(end_date.strftime('%Y-%m-%d'))
    analyzer.analyze_hist(get_blue_chip_stock_codes(), start_date_str=date_str, end_date_str=end_date.strftime('%Y-%m-%d'))
