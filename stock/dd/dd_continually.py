__author__ = 'kittaaron'
# 大单数据分析,需要先执行dd_dump.py，把当天数据导入，就可以分析了
'''
    
'''

import sys

import datetime
import logging
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.sql import func

from config import dbconfig
from model.DaDanSts import DaDanSts
from model.DaDan import DaDan
from model.HistData import HistData
from utils.holiday_util import get_pre_transact_date, get_pre_transact_date, is_holiday
import config.logginconfig
from sqlalchemy.ext.declarative import declarative_base
from stock.basic import get_by_codes
from stock.report import report_query

Base = declarative_base()

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def save(data, autocommit=True):
    session.add(data)
    if autocommit:
        session.commit()


def to_dict(pre_four_days_data):
    ret = {}
    for data in pre_four_days_data:
        ret[data.date] = data
    return ret


def get_continually_in(start_date_str, end_date_str):
    #stmt = text("select * from (select name,count(net) cnt from dd_sts where date in (:start_date_str,:end_date_str) and net > 100000 and ratio > 0.1 group by name) t where cnt > 1")
    #stmt = stmt.columns(DDCnt.name, DDCnt.cnt)
    #datas = session.query(DaDanSts).from_statement(stmt).params(start_date_str=start_date_str, end_date_str=end_date_str).all()

    datas = session.query(DaDanSts.code, func.count(DaDanSts.net).label("cnt")).\
        filter(and_(DaDanSts.date.in_([start_date_str,end_date_str]), DaDanSts.net > 900000, DaDanSts.ratio > 0.1)).\
        group_by(DaDanSts.code).having(func.count(DaDanSts.net) > 1).all()
    codes = []
    for data in datas:
        codes.append(data[0])
    dds = session.query(DaDanSts).filter(and_(DaDanSts.code.in_(codes), DaDanSts.date >= start_date_str, DaDanSts.date <= end_date_str)).all()
    hists = session.query(HistData).filter(and_(HistData.code.in_(codes), HistData.date >= start_date_str, HistData.date <= end_date_str)).all()
    hist_dict = {}
    for hist in hists:
        if hist.code not in hist_dict:
            hist_dict[hist.code] = {}
        hist_dict[hist.code][hist.date] = hist
    stockinfos = get_by_codes(codes)
    stockinfo_dict = {}
    for stockinfo in stockinfos:
        if stockinfo.code not in stockinfo_dict:
            stockinfo_dict[stockinfo.code] = stockinfo

    year = datetime.date.today().year
    reports = report_query.get_year_reports(codes, [year - 1, year - 2, year - 3])
    #report_dict = {}
    #for report in reports:
    #    if report.code not in report_dict:
    #        report_dict[report.code] = {}
    #        report_dict[report.code][report.year] = {'roe': report.roe, 'profits_yoy': report.profits_yoy, 'mbrg': report.mbrg, 'nprg': report.nprg}

    i = 0
    for dd in dds:
        p_change = hist_dict[dd.code][dd.date].p_change if dd.code in hist_dict and dd.date in hist_dict[dd.code] else None
        i += 1
        logging.info("%s %s %s net:%s ratio:%s 涨跌:%s", dd.code, dd.name, dd.date, dd.net, dd.ratio, p_change)
        if i % 3 == 0:
            logging.info("pe: %s %s", stockinfo_dict[dd.code].pe, reports[dd.code])


def get_dds_by_date(code, date_str):
    dds = session.query(DaDan).filter(and_(DaDan.code == code, DaDan.date == date_str)).all()
    return dds


def get_fhh_dds_by_date(code, date_str):
    dds = session.query(DaDan).filter(
        and_(DaDan.code == code, DaDan.date == date_str, DaDan.time >= '09:30:00', DaDan.time <= '10:00:00')).all()
    return dds


def get_ddsts_by_date(date_str):
    """
     取出某天的所有大单统计数据
    :param date_str:
    :return:
    """
    ddstss = session.query(DaDanSts).filter(DaDanSts.date == date_str).all()
    return ddstss


if __name__ == '__main__':
    argv = len(sys.argv)
    starttime = datetime.datetime.now()
    hour = starttime.hour
    delta = datetime.timedelta(days=2)
    today = datetime.date.today()
    end_date_str = today.strftime('%Y-%m-%d')

    if is_holiday(end_date_str) or hour < 10:
        end_date_str = get_pre_transact_date(today.strftime('%Y-%m-%d'))

    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
    ndays_before = end_date - delta
    start_date_str = ndays_before.strftime('%Y-%m-%d')
    logging.info("%s ~ %s", start_date_str, end_date_str)
    get_continually_in(start_date_str, end_date_str)
    endtime = datetime.datetime.now()
    logging.info((endtime - starttime).seconds)
