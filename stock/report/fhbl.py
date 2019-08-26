"""
分红比例计算
"""
from utils.db_utils import *
from model.StockInfo import StockInfo
from model.report.Fhsg import Fhsg
import tushare as ts
import config.logginconfig
import logging
import math
import time
from sqlalchemy import *

session = getSession()
pro = ts.pro_api('c4ccc5b28a49ae5f7b82d84d0d28bbc366d6f50f16bcb3cf21ae3d43')


def calc_fhsg(code, name, row):
    """
        dump分红送股数据
    :param code:
    :param name:
    :param row:
    :return
    """
    try:
        fhsgs = session.query(Fhsg).filter(and_(Fhsg.code ==  code, Fhsg.end_date.like("%1231"))).order_by(desc(Fhsg.end_date)).all()

        for fhsg_i in fhsgs:
            if fhsg_i is None or fhsg_i.cash_div == 0:
                logging.info("%s %s %s 无分红数据", code, name, fhsg_i.end_date)
                return
            # 每股分红 * 基准股本 / 总市值
            stock_info = session.query(StockInfo).filter(StockInfo.code == code).first()
            fhsg_i.cash_rate = round(fhsg_i.cash_div * fhsg_i.base_share * 100 / float(stock_info.mktcap), 2)
            logging.info("%s %s 分红率%s%%", code, name, fhsg_i.cash_rate)
            session.add(fhsg_i)
            session.commit()
    except Exception as e:
        logging.error("%s", e)


if __name__ == '__main__':
    stocks = session.query(StockInfo).all()
    #stocks = session.query(StockInfo).filter(StockInfo.code == '601636').all()
    i = 0
    for row in stocks:
        if row is None:
            continue
        code = row.code
        name = row.name
        calc_fhsg(code, name, row)