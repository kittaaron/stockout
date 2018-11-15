__author__ = 'kittaaron'
import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig

from utils.db_utils import *


def dump_today_all():
    df = ts.get_today_all()
    logging.info("get today data ok.")
    df.to_sql('today_data', engine, if_exists='append')


def get_real_time_quote_by_code(code):
    df = ts.get_realtime_quotes(code)
    for index, data in df.iterrows():
        name = data['name']
        price = float(data.price)
        price = float(data.a1_p) if price == 0 else price
        pre_close = float(data.pre_close)
        p_change = round((price - pre_close)/pre_close*100, 2)
        # 成交量
        volume = data.volume
        b1_p = data.b1_p
        b1_v = int(data.b1_v if data.b1_v else 0)
        b2_p = data.b2_p
        b2_v = int(data.b2_v if data.b2_v else 0)
        b3_p = data.b3_p
        b3_v = int(data.b3_v if data.b3_v else 0)
        b4_p = data.b4_p
        b4_v = int(data.b4_v if data.b4_v else 0)
        b5_p = data.b5_p
        b5_v = int(data.b5_v if data.b5_v else 0)

        a1_p = data.a1_p
        a1_v = int(data.a1_v if data.a1_v else 0)
        a2_p = data.a2_p
        a2_v = int(data.a2_v if data.a2_v else 0)
        a3_p = data.a3_p
        a3_v = int(data.a3_v if data.a3_v else 0)
        a4_p = data.a4_p
        a4_v = int(data.a4_v if data.a4_v else 0)
        a5_p = data.a5_p
        a5_v = int(data.a5_v if data.a5_v else 0)
        
        # 买盘合计(手数)
        b_sum = (b1_v + b2_v + b3_v + b4_v + b5_v)
        # 卖盘合计(手数)
        a_sum = (a1_v + a2_v + a3_v + a4_v + a5_v)

        logging.info("%6s 涨跌 %5s   买1 %14s   买2 %14s   买3 %14s   买4 %14s   买5 %14s 总计 %s",
                     name, p_change, str(b1_v) + "(" + b1_p + ")", str(b2_v) + "(" + b2_p + ")",
                     str(b3_v) + "(" + b3_p + ")", str(b4_v) + "(" + b4_p + ")", str(b5_v) + "(" + b5_p + ")", b_sum)
        logging.info("%6s 涨跌 %5s   卖1 %14s   卖2 %14s   卖3 %14s   卖4 %14s   卖5 %14s 总计 %s",
                     name, p_change, str(a1_v) + "(" + a1_p + ")", str(a2_v) + "(" + a2_p + ")",
                     str(a3_v) + "(" + a3_p + ")", str(a4_v) + "(" + a4_p + ")", str(a5_v) + "(" + a5_p + ")", a_sum)
        return data


def get_real_time_quote_by_codes(codes):
    df = ts.get_realtime_quotes(codes)
    ret = {}
    for index, data in df.iterrows():
        ret[data.code] = data
    return ret


if __name__ == '__main__':
    pass
