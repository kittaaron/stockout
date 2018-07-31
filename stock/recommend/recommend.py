"""
通过分析数据，给出最近推荐的股票
"""

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from config import dbconfig
from model.StockInfo import StockInfo
from model.HistData import HistData
from stock.report import risk
from stock.realtime.realtime_data import get_real_time_quote_by_codes
import datetime
from utils.SMSUtil import sendMsg

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def continually_in():
    end_date = datetime.date.today()
    total_delta = datetime.timedelta(days=7)
    start_date = end_date - total_delta
    start = start_date.strftime('%Y-%m-%d')
    end = end_date.strftime('%Y-%m-%d')
    hist_datas = session.query(HistData).filter(and_(HistData.net > 0,
                                                     HistData.date <= end,
                                                     HistData.date >= start)).all()


if __name__ == '__main__':
    pass