from typing import Any, Union

import tushare as ts
import logging
import config.logginconfig
from model.report.ReportData import ReportData
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from config import dbconfig
import math
import datetime
from dateutil.relativedelta import relativedelta
from model.HistData import HistData
from model.RealTimePE import RealTimePE
from model.RealTimePEEPS import RealTimePEEPS
import math
from model.StockInfo import StockInfo
from model.report.Zycwzb import Zycwzb
from model.report.Zcfzb import Zcfzb
from model.report.Cwbbzy import Cwbbzy
from model.report.Lrb import Lrb
from model.report.Xjllb import Xjllb
from utils.db_utils import *
import numpy as np


def get_latest_record_date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    if 1 <= month <= 4:
        year -= 1
        return str(year) + "-" + "12-31"
    elif 5 <= month <= 8:
        return str(year) + "-" + "03-31"
    elif 9 <= month <= 10:
        return str(year) + "-" + "06-30"
    elif 11 <= month:
        return str(year) + "-" + "09-30"
    else:
        return None


def get_pre_yearreport_date(date_str):
    year = int(date_str[0:4]) - 1
    return str(year) + "-" + "12-31"


def analyze():
    latest_date = get_latest_record_date()
    logging.info("latest_date: %s", latest_date)


def get_multiple(date):
    month = datetime.datetime.now().month

    date_no_year = date[(len(date) - 5):]
    if date_no_year == '03-31':
        return 4
    if date_no_year == '06-30':
        return 2
    if date_no_year == '09-30':
        return 4/3
    if date_no_year == '12-31':
        return 1


    #if 1 <= month <= 4:
        #return 1
    #elif 5 <= month <= 8:
        #return 4
    #elif 9 <= month <= 10:
        #return 2
    #elif 11 <= month:
        #return 4 / 3


def get_mean_ratio(zycwzb1, zycwzb2, zycwzb3, zycwzb4, zycwzb1_lastyear, code, name):
    """
     根据最近几年的报表，估算出未来增长率
    :param zycwzb1:
    :param zycwzb2:
    :param zycwzb3:
    :param zycwzb4:
    :param zycwzb1_lastyear:
    :param code:
    :param name:
    :return:
    """
    r = None
    if zycwzb1 is None or zycwzb2 is None or \
        zycwzb3 is None or zycwzb4 is None or zycwzb1_lastyear is None:
        return r
    if zycwzb1.npad < zycwzb1_lastyear.npad or \
            zycwzb2.npad < zycwzb3.npad or \
            zycwzb3.npad < zycwzb4.npad:
        logging.warning("%s %s 没有持续增长", code, name)
    if zycwzb1_lastyear.npad == 0 or \
            zycwzb3.npad == 0 or \
            zycwzb4.npad == 0:
        logging.info("%s %s出现净利润为0的情况", code, name)
        return 0

    r1 = int(round((float(zycwzb1.npad) - float(zycwzb1_lastyear.npad)) / float(zycwzb1_lastyear.npad), 2) * 100)
    r2 = int(round((float(zycwzb2.npad) - float(zycwzb3.npad)) / float(zycwzb3.npad), 2) * 100)
    r3 = int(round((float(zycwzb3.npad) - float(zycwzb4.npad)) / float(zycwzb4.npad), 2) * 100)

    if r1 == 0 or r2 == 0 or r3 == 0:
        logging.info("%s %s 最近有0增长出现", code, name)
        return 0

    if int(r1/r2) >= 2 or int(r2/r3) >= 2:
        logging.warning("%s %s 增长不稳定", code, name)
    # r为未来增长率，这种计算方式是估出来的
    r = int((r1 + r2 + r3) / 3 * 0.75)
    logging.info("%s %s 增长率为: %s r1: %s, r2: %s, r3: %s", code, name, r, r1, r2, r3)
    return r


def get_mean_ratio1(code, name, old):
    """
    获取平均增长率
    :param code:
    :param name:
    :return:
    """
    # 获取最近的24条财报(也就是最近6年。但是注意：新上市公司可能只有半年报和年报，数据会不准)
    zycwzbs = session.query(Zycwzb).filter(and_(Zycwzb.code == code)).order_by(desc(Zycwzb.date)).limit(24).all()
    r = None
    if zycwzbs is None:
        logging.warning("%s %s 没找到财务报表数据.", code, name)
        return r
    if len(zycwzbs) is None:
        logging.warning("%s %s 没找到最近6年的报表数据.", code, name)
        return r

    zycwzbs_dict = {}
    for zycwzb in zycwzbs:
        zycwzbs_dict[zycwzb.date] = zycwzb

    ratios = []
    i = 0
    endi = len(zycwzbs) - 4
    for zycwzb in zycwzbs:
        i += 1
        if i > endi:
            break
        npad = zycwzb.npad
        current_term = zycwzb.date
        last_term_date = str(int(current_term[0:4]) - 1) + current_term[4:]
        if last_term_date not in zycwzbs_dict:
            logging.info("%s %s %s 财报不存在", code, name, last_term_date)
            return None
        last_term_npad = zycwzbs_dict[last_term_date].npad
        diff = npad - last_term_npad
        ratio = diff/last_term_npad if last_term_npad != 0 else (0 if last_term_npad >= 0 else 0)
        ratios.append(int(ratio * 100))

    # 标准差
    std_devi = round(float(np.std(ratios, ddof=1)), 2)
    old.std_devi = std_devi
    mean_ratio = round(float(np.mean(ratios)), 2)

    logging.info("增长率: %s, 平均: %s, 标准差: %s", ratios, mean_ratio, std_devi)
    return mean_ratio



def calc_pe_eps(code, name, stock):
    logging.info("handle %s %s", code, name)
    date1 = get_latest_record_date()
    date2 = get_pre_yearreport_date(date1)
    date3 = get_pre_yearreport_date(date2)
    date4 = get_pre_yearreport_date(date3)
    zycwzb1 = session.query(Zycwzb).filter(and_(Zycwzb.code == code)).order_by(desc(Zycwzb.date)).limit(1).first()
    date1 = zycwzb1.date
    lastyear_date1 = str(int(date1[0:4]) - 1) + date1[4:]
    lastyear_date2 = str(int(date2[0:4]) - 1) + date2[4:]
    lastyear_date3 = str(int(date3[0:4]) - 1) + date3[4:]
    lastyear_date4 = str(int(date4[0:4]) - 1) + date4[4:]
    zycwzb2 = session.query(Zycwzb).filter(and_(Zycwzb.code == code, Zycwzb.date == date2)).first()
    zycwzb3 = session.query(Zycwzb).filter(and_(Zycwzb.code == code, Zycwzb.date == date3)).first()
    zycwzb4 = session.query(Zycwzb).filter(and_(Zycwzb.code == code, Zycwzb.date == date4)).first()
    old = session.query(RealTimePEEPS).filter(RealTimePEEPS.code == code).first()

    if stock.totals == 0:
        logging.info("%s total is zero.", stock)
        return

    ## 股数
    totals = stock.totals * 10000

    # 乘数：如果半年报要乘2，一季报乘4，3季报*4/3
    multiple = get_multiple(date1)
    if old is None:
        old = RealTimePEEPS(code=code, name=name)
    if zycwzb1 is not None:
        old.eps1 = float(float(zycwzb1.eps) * multiple)
        old.koufei_eps = float(round(float(zycwzb1.npad / totals) * multiple, 2))
        old.latest_report_date = zycwzb1.date

    if zycwzb2 is not None: old.eps2 = round(float(zycwzb2.npad / totals), 2)
    if zycwzb3 is not None: old.eps3 = round(float(zycwzb3.npad / totals), 2)
    if zycwzb4 is not None: old.eps4 = round(float(zycwzb4.npad / totals), 2)

    hist = session.query(HistData).filter(HistData.code == code).order_by(desc(HistData.date)).limit(1).first()
    if hist is None:
        return
    """
        这里计算eps和pe不能以历史的eps来算，因为如果出现增股 eps*total 算出来的值会不对，只能用扣非净利润算
    """
    koufei_pe = round(float(hist.close) / (old.koufei_eps), 0) if old.koufei_eps != 0 and old.koufei_eps is not None else -999
    pe1 = round(float(hist.close) / (old.eps1), 2) if old.eps1 != 0 and old.eps1 is not None else -999
    pe2 = round(float(hist.close) / old.eps2, 2) if old.eps2 != 0 and old.eps2 is not None else -999
    pe3 = round(float(hist.close) / old.eps3, 2) if old.eps3 != 0 and old.eps3 is not None else -999
    pe4 = round(float(hist.close) / old.eps4, 2) if old.eps4 != 0 and old.eps4 is not None else -999
    old.koufei_pe = koufei_pe
    old.pe1 = pe1
    old.pe2 = pe2
    old.pe3 = pe3
    old.pe4 = pe4
    old.date = hist.date
    old.price = hist.close
    # eval_pe = E * (8.5 + 2 * R)  或者 股价=E*(2R+8.5)*4.4/Y (Y为国债利率)

    #r = getr(zycwzb1, zycwzb2, zycwzb3, zycwzb4, zycwzb1_lastyear, code, name)
    mean_ratio = get_mean_ratio1(code, name, old)
    if old.koufei_eps < 0 or mean_ratio is None:
        old.eval_price = 0
        old.eval_price_ratio = 0
    else:
        old.eval_price = round(old.koufei_eps * (8.5 + 2*mean_ratio), 2)
        old.eval_price_ratio = round(old.eval_price / float(old.price), 2)

    save(old)


if __name__ == '__main__':
    stocks = session.query(StockInfo).all()
    #stocks = session.query(StockInfo).filter(StockInfo.code == '600516').all()
    for row in stocks:
        if row is None:
            continue
        code = row.code
        name = row.name
        calc_pe_eps(code, name, row)
