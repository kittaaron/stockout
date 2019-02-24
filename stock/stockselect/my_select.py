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
    selected_stocks = getSession().query(Select).filter().all()
    codes = []

    for selected in selected_stocks:
        codes.append(selected.code)
    return codes


def get_all_select():
    selected_stocks = getSession().query(Select).filter().all()
    return selected_stocks


def get_all_select_map():
    ret = {}
    selected_stocks = get_all_select()
    for selected_stock in selected_stocks:
        ret[selected_stock.code] = selected_stock
    return ret


if __name__ == '__main__':
    pass
