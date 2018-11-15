__author__ = 'kittaaron'

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig
from stock.report import xsjj
import datetime
from dateutil.relativedelta import relativedelta
from utils.db_utils import *


def risk_warning(code):
    """
    股票风险警示：限售解禁等
    :param code:
    :return:
    """
    xsjj_datas = xsjj_warnging(code)
    if len(xsjj_datas) > 0:
        for xsjj_data in xsjj_datas:
            logging.info("%s", xsjj_data)
        return True
    else:
        return False


def xsjj_warnging(code):
    """
        五个月内是否有限售解禁股票
    :param code:
    :return:
    """
    startdate = datetime.date.today()
    enddate = datetime.date.today() + relativedelta(months=+6)
    xsjj_datas = xsjj.get_xsjj_by_code_time(code, startdate, enddate)
    return xsjj_datas


if __name__ == '__main__':
    risk_warning("002195")