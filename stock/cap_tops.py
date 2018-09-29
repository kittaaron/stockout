__author__ = 'kittaaron'
# 个股上榜统计

import tushare as ts
import config.logginconfig
import logging
from config import dbconfig
import datetime
from utils.db_utils import *


def get_cap_tops():

    df = ts.cap_tops()
    df.to_sql('cap_tops', engine, if_exists='append', index=False, index_label='code')


if __name__ == '__main__':
    get_cap_tops()