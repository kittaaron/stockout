__author__ = 'kittaaron'
# 机构席位追踪

import tushare as ts
import config.logginconfig
import logging
from config import dbconfig
import datetime
from utils.db_utils import *


def get_inst_detail():
    df = ts.inst_detail()
    df.to_sql('inst_detail', engine, if_exists='replace', index=False, index_label='code')


if __name__ == '__main__':
    get_inst_detail()