__author__ = 'kittaaron'
# 已选大单数据

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from config import dbconfig
import datetime
from model.Select import Select
from stock.select import analyzer

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def get_select_codes():
    codes = []
    selected_stocks = session.query(Select).filter().all()
    for selected in selected_stocks:
        codes.append(selected.code)
    return codes


def analyse_selected_dd(date_str):
    codes = get_select_codes()
    analyzer.analyze_codes_dd(codes, date_str)


if __name__ == '__main__':
    end_date = datetime.date.today()
    total_delta = datetime.timedelta(days=0)
    start_date = end_date - total_delta
    date_str = start_date.strftime('%Y-%m-%d')

    analyse_selected_dd(date_str)
