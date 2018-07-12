__author__ = 'kittaaron'
# 默认dump当天所有股票的大单数据列表，并给出统计结果

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
from model.HistData import HistData
from utils.SMSUtil import sendMsg

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()

RANGE = -9.00


def realtime_dd_analysis(code, name, date_str):
    # 如果查到没有大单数据，也应该往数据库写一条假数据，保证下次不再查
    df = ts.get_sina_dd(code, date_str)
    # logging.info(df)
    if df is None:
        return

    bvolume = 0
    svolume = 0
    #lhhbvolume = 0
    #lhhsvolume = 0
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
            #if '14:30:00' < serie.time <= '14:59:59':
                #lhhbvolume += serie.volume
        if serie.type == '卖盘':
            svolume += serie.volume
            #if '14:30:00' <= serie.time <= '14:59:59':
                #lhhsvolume += serie.volume

    net = bvolume - svolume
    #lhh_net = lhhbvolume - lhhsvolume
    dd_sts = DaDanSts(code=code, name=name, date=date_str)
    dd_sts.b_volume = bvolume
    dd_sts.s_volume = svolume
    dd_sts.net = net
    #dd_sts.lhh_b_volume = lhhbvolume
    #dd_sts.lhh_s_volume = lhhsvolume
    #dd_sts.lhh_net = lhh_net
    logging.info("%s %s 买盘：%d, 卖盘：%d, 总计：%d", code, name, bvolume, svolume, net)
    if net > 1000000:
        logging.info("OOOOOOOOOOOOOOOOOOOOO  %s %s 大单净流入 %d 请关注实时大单数据，可能在撬盘 OOOOOOOOOOOOOOOOOOOOO", code, name, net)
        sms_msg = code + " may be qiaopan"
        sendMsg(sms_msg)
    return dd_sts


def analyze_dieting_stocks(hist_data, date_str):
    end_time = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    start_time = end_time - datetime.timedelta(days=15)
    start_time_str = start_time.strftime('%Y-%m-%d')
    # 每支股票、获取前10天数据，统计跌停次数
    for data in hist_data:
        code = data.code
        # 股票名称
        name = data.name
        i = 0
        dieting_dates = []
        latest_10_days_data = session.query(HistData).filter(
            and_(HistData.code == code, HistData.date <= date_str, HistData.date >= start_time_str)).all()
        if hist_data is None or len(latest_10_days_data) <= 0:
            logging.info("%s %s 获取最近10天数据出错", code, name)
        for date_data in latest_10_days_data:
            if date_data.p_change <= RANGE:
                i += 1
                dieting_dates.append(date_data.date)
        # 当日大单数据分析.
        dd_sts = session.query(DaDanSts).filter(and_(DaDanSts.code == code, DaDanSts.date == date_str)).first()
        if dd_sts is None:
            logging.info("%s %s 跌停天数 %d, 日期: %s 无大单统计数据",
                         code, name, i, str(dieting_dates))
        else:
            logging.info("%s %s 跌停天数 %d, 日期: %s 全天买入:%d, 卖出:%d, 净值:%d, 最后半小时净值:%d, 大单占市值比:%d",
                         code, name, i, str(dieting_dates),
                         dd_sts.b_volume, dd_sts.s_volume, dd_sts.net, dd_sts.lhh_net, dd_sts.ratio)
            if dd_sts.ratio >= 3 or dd_sts.net >= 5000000 or dd_sts.lhh_net >= 5000000:
                logging.info("****************** 撬板的真来了 %s %s *********************", code, name)
            if dd_sts.ratio >= 1 or dd_sts.net >= 1000000 or dd_sts.lhh_net >= 1000000:
                logging.info("******************注意：可能撬板的来了 %s %s ***************", code, name)

        realtime_dd_analysis(code, name, date_str)



def get_dieting_stocks(date_str):
    '''
    实时获取当天大单数据，不存到DB，直接内存统计并打印
    :return:
    '''

    # 取出某日期跌幅 >= 9%的股票
    hist_data = session.query(HistData).filter(
        and_(HistData.date == date_str, HistData.p_change <= RANGE)).all()

    if hist_data is None or len(hist_data) <= 0:
        logging.info("没有跌幅超过 %d 的股票", RANGE)
        return None
    logging.info("------------跌停股票数量: %d", len(hist_data))
    analyze_dieting_stocks(hist_data, date_str)


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    delta = datetime.timedelta(days=0)
    today = datetime.date.today()
    ndays_before = today - delta
    date_str = ndays_before.strftime('%Y-%m-%d')

    get_dieting_stocks(date_str)

    end_time = datetime.datetime.now()
    logging.info((end_time - start_time).seconds)
