__author__ = 'kittaaron'
# 基金持股

import tushare as ts
import config.logginconfig
import logging

from utils.db_utils import *


def get_jjcg():
    df = ts.fund_holdings(2018, 2)
    df.to_sql('jjcg', engine, if_exists='append', index=False, index_label='code')


if __name__ == '__main__':
    get_jjcg()