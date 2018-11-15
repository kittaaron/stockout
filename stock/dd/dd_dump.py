__author__ = 'kittaaron'
# 默认dump当天所有股票的大单数据列表，并给出统计结果

import tushare as ts
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy import func
import config.dbconfig as dbconfig
import config.logginconfig
import datetime
from model.StockInfo import StockInfo
from model.DaDan import DaDan
from model.DaDanSts import DaDanSts
from utils.holiday_util import get_pre_transact_date
from utils.holiday_util import is_holiday
import sys
from utils.db_utils import *


def save_list(datas, autocommit=True):
    session.add_all(datas)
    if autocommit:
        session.commit()


def dump_stock_dd_by_date(code, name, totals, date_str):
    dds = session.query(DaDanSts).filter(and_(DaDan.code == code, DaDan.date == date_str)).first()
    if dds is not None:
        return

    # 如果查到没有大单数据，也应该往数据库写一条假数据，保证下次不再查
    df = ts.get_sina_dd(code, date_str)
    # logging.info(df)
    if df is None:
        return

    bvolume = 0
    svolume = 0
    fhhbvolume = 0
    fhhsvolume = 0
    lhhbvolume = 0
    lhhsvolume = 0
    da_dan_list = []
    for index, serie in df.iterrows():
        da_dan = DaDan(code=code, name=name, date=date_str)
        da_dan.time = serie.time
        da_dan.type = serie.type
        da_dan.volume = serie.volume
        da_dan.price = serie.price
        da_dan.preprice = serie.preprice
        da_dan_list.append(da_dan)

        if serie.type == '买盘':
            bvolume += serie.volume
            if '14:30:00' < serie.time <= '14:59:59':
                lhhbvolume += serie.volume
            if '09:30:00' <= serie.time <= '10:00:00':
                fhhbvolume += serie.volume
        if serie.type == '卖盘':
            svolume += serie.volume
            if '14:30:00' <= serie.time <= '14:59:59':
                lhhsvolume += serie.volume
            if '09:30:00' <= serie.time <= '10:00:00':
                fhhsvolume += serie.volume

    save_list(da_dan_list)
    net = bvolume - svolume
    lhh_net = lhhbvolume - lhhsvolume
    fhh_net = fhhbvolume - fhhsvolume
    ratio = net / totals / 1000000
    lhh_ratio = lhh_net / totals / 1000000
    dd_sts = DaDanSts(code=code, name=name, date=date_str)
    dd_sts.b_volume = bvolume
    dd_sts.s_volume = svolume
    dd_sts.net = net
    dd_sts.lhh_b_volume = lhhbvolume
    dd_sts.lhh_s_volume = lhhsvolume
    dd_sts.lhh_net = lhh_net
    dd_sts.ratio = ratio
    dd_sts.lhh_ratio = lhh_ratio

    dd_sts.fhh_b_volume = fhhbvolume
    dd_sts.fhh_s_volume = fhhsvolume
    dd_sts.fhh_net = fhh_net
    logging.info("%s %s 买盘：%d, 卖盘：%d, 总计：%d", code, name, bvolume, svolume, net)
    logging.info("%s %s 最后半小时- 买盘：%d, 卖盘：%d, 总计：%d", code, name, lhhbvolume, lhhsvolume, lhh_net)
    save(dd_sts)


def dump_dd(date_str):
    '''
    dump_dd dump当天的大单数据，如果数据库已有，则不获取
    :return:
    '''
    codes = ['603843', '002219']
    # code = '603843' # 正平股份
    # code = '002219' # 恒康医疗

    stocks = session.query(StockInfo).all()

    i = 1
    for row in stocks:
        if row is None:
            continue
        # 股票代码
        code = row.code
        # 股票名称
        name = row.name
        # 总股本
        totals = row.totals
        logging.info("%s %s 开始处理 - %d", code, name, i)
        i += 1
        dump_stock_dd_by_date(code, name, totals, date_str)


def get_start_date():
    max_date_indb = session.query(func.max(DaDanSts.date)).first()
    max_date_indb = max_date_indb[0] if max_date_indb is not None else "2005-12-31"
    return datetime.datetime.strptime(max_date_indb, '%Y-%m-%d') + datetime.timedelta(days=1)


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    hour = starttime.hour

    endday = datetime.date.today()
    if hour < 15:
        # 9点前dump前一天的，否则默认dump今天的
        endday = datetime.datetime.strptime(get_pre_transact_date(endday.strftime('%Y-%m-%d')), '%Y-%m-%d')

    startday = get_start_date()

    argv = len(sys.argv)
    if argv > 2:
        startday = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
        endday = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')

    logging.info("startday: %s, endday: %s", startday, endday)
    while startday <= endday:
        date_str = startday.strftime('%Y-%m-%d')
        if is_holiday(date_str):
            startday += datetime.timedelta(days=1)
            continue
        logging.info("date: %s", date_str)
        dump_dd(date_str)
        startday += datetime.timedelta(days=1)

    endtime = datetime.datetime.now()
    logging.info("导入 %s 日大单数据耗时 %d 秒", date_str, (endtime - starttime).seconds)
