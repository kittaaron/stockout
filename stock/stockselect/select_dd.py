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
from stock.stockselect import analyzer
from stock.basic import get_codes_by_names
from utils.db_utils import *


def get_select_codes():
    selected_stocks = session.query(Select).filter().all()
    names = []

    for selected in selected_stocks:
        names.append(selected.name)
    return get_codes_by_names(names)


def analyse_selected_dd(date_str):
    codes = get_select_codes()
    analyzer.analyze_codes_dd(codes, date_str, False)


if __name__ == '__main__':
    end_date = datetime.date.today()
    total_delta = datetime.timedelta(days=0)
    start_date = end_date - total_delta
    date_str = start_date.strftime('%Y-%m-%d')

    analyse_selected_dd(date_str)
