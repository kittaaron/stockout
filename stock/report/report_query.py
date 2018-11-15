__author__ = 'kittaaron'

import tushare as ts
import logging
import config.logginconfig
from model.report.ReportData import ReportData
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from config import dbconfig
import math
import datetime
from dateutil.relativedelta import relativedelta
from utils.db_utils import *


def get_year_reports(codes, years):
    """
    获取年报(第4季度报表)
    :param codes:
    :param years:
    :return: {code: {year: {}, year2: {}}, ...}
    """
    if len(codes) <= 0 or len(years) <= 0:
        return None

    ret = {}
    for code in codes:
        ret[code] = {}
        for year in years:
            ret[code][year] = ReportData()
    reports = session.query(ReportData).filter(and_(ReportData.code.in_(codes),
                                                    ReportData.year.in_(years), ReportData.season == 4)).order_by(
            desc(ReportData.year)).all()
    for report in reports:
        code = report.code
        year = report.year
        roe = float(report.roe) if report.roe is not None else None
        profits_yoy = float(report.profits_yoy) if report.profits_yoy is not None else None
        mbrg = float(report.mbrg) if report.mbrg is not None else None
        nprg = float(report.nprg) if report.nprg is not None else None
        net_profits = float(report.net_profits) if report.net_profits is not None else None
        if code not in ret:
            ret[code] = {}
        ret[code][year] = {'roe': roe, 'profits_yoy': profits_yoy, 'mbrg': mbrg, 'nprg': nprg, 'net_profits': net_profits}
    return ret


def get_latest_report(code):
    """
    获取年报(第4季度报表)
    :param codes:
    :param years:
    :return:
    """
    year = datetime.date.today().year
    month = datetime.date.month
    if month >= 5 and month <= 8:
        season = 1
    elif month >= 9 and month <= 10:
        season = 2
    elif month >= 11:
        season = 3
    else:
        year -= 1
        season = 4
    report = session.query(ReportData).filter(ReportData.code == code).first()
    return report


if __name__ == '__main__':
    pass
