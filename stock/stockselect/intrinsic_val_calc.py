"""
    计算公司内在价值
"""

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
from stock.stockselect.my_select import *
from stock.basic import get_codes_by_names
from utils.db_utils import *
from stock.report.report_query import *
from stock.basic import get_by_code
from utils.SMSUtil import *

session = getSession()

DISCOUNT_RATE = 6

def handle_select_i(selected_i):
    code = selected_i.code
    name = selected_i.name
    inc_years = selected_i.inc_years
    # 增长率
    inc_rate = selected_i.inc_rate
    # 永续增长率
    inc_perpetual = selected_i.inc_perpetual
    if inc_years is None or inc_rate is None or  inc_perpetual is None:
        #logging.info("%s 没有找到增长率配置", name)
        return
    if inc_years == 0 and inc_rate == 0 and inc_perpetual == 0:
        #logging.info("%s 没有找到增长率配置", name)
        return
    if inc_perpetual >= DISCOUNT_RATE:
        #print("%s 永续增长率必须小于贴现率", name)
        return

    a1 = (100 + inc_rate) / (100 + DISCOUNT_RATE)
    latest_year_zycwzb = get_latest_year_zycwzb(code)
    npad = int(latest_year_zycwzb.npad)
    # 等比数列公式
    val1 = int(npad * a1 * (1 - pow(a1, inc_years)) / (1 - a1)) if a1 != 1 else a1 * inc_years
    # 计算n年后的价值，再贴现到今日
    val2 = int((npad * pow(a1, inc_years) * 100 / (DISCOUNT_RATE - inc_perpetual)) * pow((100 - DISCOUNT_RATE) / 100, inc_years))

    stockinfo = get_by_code(code)
    mktcap = float(stockinfo.mktcap)

    intrincsic_val = int((val1 + val2) / 10000)
    current_discount = round(mktcap / (val1 + val2), 2)
    logging.info("%s 内在价值 %s 亿，当前折扣率： %s", name, intrincsic_val, current_discount)
    if current_discount < 0.5:
        params = [name]
        sendIntrinsicDiscountMsgTX(params)
        logging.info("%s 发送通知成功", name)


def select_intrinsic_calc():
    selected_stocks = get_all_select()
    for selected_i in selected_stocks:
        handle_select_i(selected_i)

if __name__ == '__main__':
    select_intrinsic_calc()