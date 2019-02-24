__author__ = 'kittaaron'
# 实时取当天所有股票的大单数据列表，并给出统计结果

import tushare as ts
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
import config.dbconfig as dbconfig
import config.logginconfig
import datetime
from model.StockInfo import StockInfo
from model.DaDan import DaDan
from model.DaDanSts import DaDanSts

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def stock_dd_sts_by_date(code, name, totals, date_str):
    # 如果查到没有大单数据，也应该往数据库写一条假数据，保证下次不再查
    df = ts.get_sina_dd(code, date_str)
    # logging.info(df)
    if df is None:
        return

    bvolume = 0
    svolume = 0
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
        if serie.type == '卖盘':
            svolume += serie.volume
            if '14:30:00' <= serie.time <= '14:59:59':
                lhhsvolume += serie.volume

    net = bvolume - svolume
    if net <= 1000000:
        return None
    lhh_net = lhhbvolume - lhhsvolume
    ratio = round(net / totals / 1000000, 2)
    dd_sts = DaDanSts(code=code, name=name, date=date_str)
    dd_sts.b_volume = bvolume
    dd_sts.s_volume = svolume
    dd_sts.net = net
    dd_sts.lhh_b_volume = lhhbvolume
    dd_sts.lhh_s_volume = lhhsvolume
    dd_sts.lhh_net = lhh_net
    dd_sts.ratio = ratio
    #dd_sts.lhh_ratio = lhh_ratio
    logging.info("%s %s 买盘：%d, 卖盘：%d, 总计：%d", code, name, bvolume, svolume, net)
    #logging.info("%s %s 最后半小时- 买盘：%d, 卖盘：%d, 总计：%d", code, name, lhhbvolume, lhhsvolume, lhh_net)
    return dd_sts


def realtime_dd(date_str):
    '''
    实时获取当天大单数据，不存到DB，直接内存统计并打印
    :return:
    '''
    stocks = getSession().query(StockInfo).all()

    i = 1
    sts_list = []
    for row in stocks:
        if row is None:
            continue
        # 股票代码
        code = row.code
        # 股票名称
        name = row.name
        # 总股本
        totals = row.totals
        if i % 50 == 0:
            logging.info("%s %s 开始处理 - %d", code, name, i)
        i += 1
        sts = stock_dd_sts_by_date(code, name, totals, date_str)
        if sts is None:
            continue
        sts_list.append(sts)
    #logging.info("大于100万手的股票数量: %d", len(sts_list))
    sorted_list = sorted(sts_list, key=lambda r: r.net, reverse=True)
    lhh_sorted_result = sorted(sts_list, key=lambda r: r.net, reverse=True)

    logging.info("大单数据总排名前20的数据: ")
    top20 = sorted_list[0:20]
    logging.info("最后半小时总排名前20的数据: ")
    lhhtop50 = lhh_sorted_result[0:50]

    lhhtop50_codes = []
    for lhhdata in lhhtop50:
        lhhtop50_codes.append(lhhdata.code)
    index = 0
    for data in top20:
        index += 1
        llh_index = -1
        try:
            llh_index = lhhtop50_codes.index(data.code)
        except ValueError as err:
            pass

        if llh_index >= 0:
            logging.info("%s %s 总数据排名: %d, 最后半小时排名: %d, %s", data.code, data.name, index, llh_index + 1, data)
        else:
            logging.info("%s %s 总数据排名: %d, 最后半小时未排进前50", data.code, data.name, index)


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    delta = datetime.timedelta(days=0)
    today = datetime.date.today()
    ndays_before = today - delta
    date_str = ndays_before.strftime('%Y-%m-%d')
    logging.info("date: %s", date_str)

    realtime_dd(date_str)

    endtime = datetime.datetime.now()
    logging.info((endtime - starttime).seconds)
