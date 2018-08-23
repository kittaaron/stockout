__author__ = 'kittaaron'
# 大单数据

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from config import dbconfig
import datetime
from model.StockInfo import StockInfo
from model.DaDan import DaDan
from model.DaDanSts import DaDanSts

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def get_ddsts_by_code_date(code, start_date_str, end_date_str):
    """
     取出某支股票，开始到截止日期的大单统计数据
    :param date_str:
    :return:
    """
    ddstss = session.query(DaDanSts).filter(and_(DaDanSts.code == code,
                                                 DaDanSts.date >= start_date_str,
                                                 DaDanSts.date <= end_date_str)).order_by(desc(DaDanSts.date)).all()
    return ddstss


def get_ddsts_by_date(date_str, order_by = None, limit = 20):
    """
     取出某日大单排名
    :param date_str:
    :return:
    """
    if limit > 100:
        limit = 100
    ddstss = session.query(DaDanSts).filter(DaDanSts.date == date_str).order_by(
        desc(DaDanSts.ratio if order_by == 'ratio' else DaDanSts.net)).limit(limit).all()
    return ddstss


def stock_dd_sts(code, name, date_str, sts_result, last_half_hour_sts_result):
    df = ts.get_sina_dd(code, date_str)
    if df is None:
        return None

    bvolume = 0
    svolume = 0
    lhhbvolume = 0
    lhhsvolume = 0
    for index, serie in df.iterrows():
        if serie.type == '买盘':
            bvolume += serie.volume
            if '14:30:00' < serie.time <= '14:59:59':
                lhhbvolume += serie.volume
        if serie.type == '卖盘':
            svolume += serie.volume
            if '14:30:00' <= serie.time <= '14:59:59':
                lhhsvolume += serie.volume

    net = (bvolume - svolume)
    lhh_net = lhhbvolume - lhhsvolume
    total_volume_data = {'code': code, "name": name, "bvolume": bvolume, "svolume": svolume, "net": net}
    lhh_volume_data = {'code': code, "name": name, "bvolume": lhhbvolume, "svolume": lhhsvolume, "net": lhh_net}
    sts_result.append(total_volume_data)
    last_half_hour_sts_result.append(lhh_volume_data)
    return 1


def get_dd():
    stocks = session.query(StockInfo).all()
    # df = ts.get_stock_basics()

    end_date = datetime.date.today()
    total_delta = datetime.timedelta(days=0)
    start_date = end_date - total_delta

    sts_result = []
    last_half_hour_sts_result = []
    tmp_date = start_date
    while tmp_date <= end_date:
        i = 0
        for row in stocks:
            if row is None:
                continue
            # 股票代码
            code = row.code
            # 股票名称
            name = row.name
            #if code not in ['603843', '000001', '000333', '000839', '000848', '000858', '002027', '601360', '601933']:
            #    continue

            date_str = tmp_date.strftime('%Y-%m-%d')
            one = stock_dd_sts(code, name, date_str, sts_result, last_half_hour_sts_result)
            if one is None:
                continue
            i += 1
            logging.info("code: %s, name: %s, date: %s, - %d", code, name, date_str, i)

        sorted_result = sorted(sts_result, key=lambda r: r['net'], reverse=True)
        lhh_sorted_result = sorted(last_half_hour_sts_result, key=lambda r: r['net'], reverse=True)
        logging.info("大单数据总排名前100的数据: ")
        top100 = sorted_result[0:100]
        logging.info(top100)
        logging.info("最后半小时总排名前100的数据: ")
        lhhtop100 = lhh_sorted_result[0:300]
        logging.info(lhhtop100)

        lhhtop100_codes = []
        for lhhdata in lhhtop100:
            lhhtop100_codes.append(lhhdata['code'])
        index = 0
        for data in top100:
            index += 1
            llh_index = -1
            try:
                llh_index = lhhtop100_codes.index(data['code'])
            except ValueError as err:
                pass

            if llh_index >= 0:
                logging.info("%s %s 总数据排名: %d, 最后半小时排名: %d, %s", data['code'], data['name'], index, llh_index + 1, data)
            else:
                logging.info("%s %s 总数据排名: %d, 最后半小时未排进前300", data['code'], data['name'], index)
            #df = ts.get_sina_dd(data['code'], tmp_date.strftime('%Y-%m-%d'))
            #df.to_sql('dd', engine, if_exists='append', index=False, index_label='code')

        tmp_date += datetime.timedelta(days=1)


def get_top_dd_sts(date_str):
    top100 = session.query(DaDanSts).filter(DaDanSts.date == date_str).order_by(desc(DaDanSts.net)).limit(100).all()
    llhtop300 = session.query(DaDanSts).filter(DaDanSts.date == date_str).order_by(desc(DaDanSts.lhh_net)).limit(300).all()
    ratiotop100 = session.query(DaDanSts).filter(DaDanSts.date == date_str).order_by(desc(DaDanSts.ratio)).limit(100).all()

    lhhtop300_codes = []
    for lhhdata in llhtop300:
        lhhtop300_codes.append(lhhdata.code)

    index = 0
    for data in top100:
        index += 1
        llh_index = -1
        try:
            llh_index = lhhtop300_codes.index(data.code)
        except ValueError as err:
            pass

        if llh_index >= 0:
            logging.info("%s %s 总数据排名: %d, 最后半小时排名: %d, %s", data.code, data.name, index, llh_index + 1, data)
        else:
            logging.info("%s %s 总数据排名: %d, 最后半小时未排进前300", data.code, data.name, index)


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    get_top_dd_sts('2018-07-11')
    endtime = datetime.datetime.now()
    logging.info((endtime - starttime).seconds)
