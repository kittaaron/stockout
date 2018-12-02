__author__ = 'kittaaron'
# 新股

import tushare as ts
import config.logginconfig
import logging
from utils import db_utils

"""
获取新股
"""

def new_stocks():
    df = ts.new_stocks()
    df.to_sql('new_stocks', db_utils.engine, if_exists='append', index=False, index_label='code')


if __name__ == '__main__':
    new_stocks()