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

from config import dbconfig
from model.DaDanSts import DaDanSts
from model.DaDan import DaDan
from model.HistData import HistData
from utils.holiday_util import get_next_transact_date, get_pre_transact_date
import config.logginconfig

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def save(data, autocommit=True):
    session.add(data)
    if autocommit:
        session.commit()


def to_dict(next_four_days_data):
    ret = {}
    for data in next_four_days_data:
        ret[data.date] = data
    return ret


def handle_one(data, date_str, index, fhh_index, lhh_index, next_tran_date, next_two_tran_date, next_three_tran_date,
               next_four_tran_date):
    # 后四天的涨跌数据
    day_data = session.query(HistData).filter(and_(HistData.code == data.code, HistData.date == date_str)).first()
    next_day_data = session.query(HistData).filter(
        and_(HistData.code == data.code, HistData.date == next_tran_date)).first()
    next_two_day_data = session.query(HistData).filter(
        and_(HistData.code == data.code, HistData.date == next_two_tran_date)).first()
    next_three_day_data = session.query(HistData).filter(
        and_(HistData.code == data.code, HistData.date == next_three_tran_date)).first()
    next_four_day_data = session.query(HistData).filter(
        and_(HistData.code == data.code, HistData.date == next_four_tran_date)).first()

    p_change = day_data.p_change if day_data is not None else None
    nex_day_p_change = next_day_data.p_change if next_day_data is not None else None
    nex_two_day_p_change = next_two_day_data.p_change if next_two_day_data is not None else None
    nex_three_day_p_change = next_three_day_data.p_change if next_three_day_data is not None else None
    nex_four_day_p_change = next_four_day_data.p_change if next_four_day_data is not None else None

    # 后四天的大单统计数据
    arr = [next_tran_date, next_two_tran_date, next_three_tran_date, next_four_tran_date]
    next_four_days_data = session.query(DaDanSts).filter(and_(DaDanSts.code == data.code, DaDanSts.date.in_(arr))).all()
    next_four_days_dict = to_dict(next_four_days_data)

    ## 后4天净流入
    next_day_net = next_four_days_dict[next_tran_date].net if next_tran_date in next_four_days_dict else None
    next_two_day_net = next_four_days_dict[
        next_two_tran_date].net if next_two_tran_date in next_four_days_dict else None
    next_three_day_net = next_four_days_dict[
        next_three_tran_date].net if next_three_tran_date in next_four_days_dict else None
    next_four_day_net = next_four_days_dict[
        next_four_tran_date].net if next_four_tran_date in next_four_days_dict else None

    ## 后4天前半小时流入
    next_day_fhh_net = next_four_days_dict[next_tran_date].fhh_net if next_tran_date in next_four_days_dict else None
    next_two_day_fhh_net = next_four_days_dict[
        next_two_tran_date].fhh_net if next_two_tran_date in next_four_days_dict else None
    next_three_day_fhh_net = next_four_days_dict[
        next_three_tran_date].fhh_net if next_three_tran_date in next_four_days_dict else None
    next_four_day_fhh_net = next_four_days_dict[
        next_four_tran_date].fhh_net if next_four_tran_date in next_four_days_dict else None

    logging.info("%s %s 排名: %d, fhh排名: %s lhh排名:%s, 净流入:%s 涨跌:%s fhh_net: %s",
                 data.code, data.name, index, fhh_index + 1 if fhh_index >= 0 else '>300', lhh_index + 1 if lhh_index >= 0 else '>300', data.net, p_change, data.fhh_net)
    logging.info("后一天净流入:%s 前半小时: %s 涨跌:%s", next_day_net, next_day_fhh_net, nex_day_p_change)
    logging.info("后二天净流入:%s 前半小时: %s 涨跌:%s", next_two_day_net, next_two_day_fhh_net, nex_two_day_p_change)
    logging.info("后三天净流入:%s 前半小时: %s 涨跌:%s", next_three_day_net, next_three_day_fhh_net, nex_three_day_p_change)
    logging.info("后四天净流入:%s 前半小时: %s 涨跌:%s", next_four_day_net, next_four_day_fhh_net, nex_four_day_p_change)


def get_top_dd_sts(date_str):
    top100 = session.query(DaDanSts).filter(DaDanSts.date == date_str).order_by(desc(DaDanSts.net)).limit(50).all()
    lhhtop300 = session.query(DaDanSts).filter(DaDanSts.date == date_str).order_by(desc(DaDanSts.lhh_net)).limit(300).all()
    fhhtop300 = session.query(DaDanSts).filter(DaDanSts.date == date_str).order_by(desc(DaDanSts.fhh_net)).limit(300).all()
    ratiotop100 = session.query(DaDanSts).filter(DaDanSts.date == date_str).order_by(desc(DaDanSts.ratio)).limit(
        100).all()
    lhhratiotop300 = session.query(DaDanSts).filter(DaDanSts.date == date_str).order_by(desc(DaDanSts.lhh_ratio)).limit(
        100).all()

    lhhtop300_codes = []
    fhhtop300_codes = []
    for lhhdata in lhhtop300:
        lhhtop300_codes.append(lhhdata.code)
    for fhhdata in fhhtop300:
        fhhtop300_codes.append(fhhdata.code)

    next_tran_date = get_next_transact_date(date_str)
    next_two_tran_date = get_next_transact_date(next_tran_date)
    next_three_tran_date = get_next_transact_date(next_two_tran_date)
    next_four_tran_date = get_next_transact_date(next_three_tran_date)

    index = 0
    for data in top100:
        index += 1
        lhh_index = -1
        fhh_index = -1
        try:
            lhh_index = lhhtop300_codes.index(data.code)
        except ValueError as err:
            pass
        try:
            fhh_index = fhhtop300_codes.index(data.code)
        except ValueError as err:
            pass

        handle_one(data, date_str, index, fhh_index, lhh_index, next_tran_date, next_two_tran_date, next_three_tran_date,
                   next_four_tran_date)

    logging.info("------------------------------------------------------------------")
    ratiolhhtop300_codes = []
    for lhhdata in lhhratiotop300:
        ratiolhhtop300_codes.append(lhhdata.code)
    index2 = 0
    for data in ratiotop100:
        index2 += 1
        fhh_index2 = -1
        lhh_index2 = -1
        try:
            lhh_index2 = ratiolhhtop300_codes.index(data.code)
            lhh_index2 = ratiolhhtop300_codes.index(data.code)
        except ValueError as err:
            pass

        handle_one(data, date_str, index2, fhh_index2, lhh_index2, next_tran_date, next_two_tran_date, next_three_tran_date,
                   next_four_tran_date)

    i2 = 1
    # for data in ratiotop100:
    #    logging.info("大单占比排名第%d %s %s 比例 %s", i2, data.code, data.name, data.ratio)
    #    i2 += 1


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


def update_fhh():
    delta = datetime.timedelta(days=0)
    endday = datetime.datetime.strptime('2018-07-13', '%Y-%m-%d')
    startday = endday - delta
    while startday <= endday:
        date_str = startday.strftime('%Y-%m-%d')
        ddstss = get_ddsts_by_date(date_str)
        for ddsts in ddstss:
            code = ddsts.code
            dds = get_fhh_dds_by_date(code, date_str)
            fhh_bvolume = 0
            fhh_svolume = 0
            fhh_net = 0
            for dd in dds:
                if dd.type == '卖盘':
                    fhh_svolume += dd.volume
                elif dd.type == '买盘':
                    fhh_bvolume += dd.volume
            fhh_net = fhh_bvolume - fhh_svolume
            ddsts.fhh_b_volume = fhh_bvolume
            ddsts.fhh_s_volume = fhh_svolume
            ddsts.fhh_net = fhh_net
            logging.info("%s %s save ok.", date_str, code)
            save(ddsts)

        startday += datetime.timedelta(days=1)


if __name__ == '__main__':
    argv = len(sys.argv)
    starttime = datetime.datetime.now()
    hour = starttime.hour
    delta = datetime.timedelta(days=1)
    today = datetime.date.today()
    ndays_before = today - delta
    date_str = today.strftime('%Y-%m-%d')
    if hour < 9:
        date_str = get_pre_transact_date(today.strftime('%Y-%m-%d'))
    #date_str = ndays_before.strftime('%Y-%m-%d')
    if argv > 1:
        date_str = sys.argv[1]
    logging.info("分析日期: %s", date_str)
    get_top_dd_sts(date_str)
    endtime = datetime.datetime.now()
    logging.info((endtime - starttime).seconds)
