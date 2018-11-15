__author__ = 'kittaaron'
# 已选大单数据

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig
from stock.stockselect import select_dd
from stock.realtime.realtime_data import get_real_time_quote_by_code

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


if __name__ == '__main__':
    codes = select_dd.get_select_codes()
    for code in codes:
        get_real_time_quote_by_code(code)
