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

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()

RANGE = 9.00


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
            if date_data.p_change >= RANGE:
                i += 1
                dieting_dates.append(date_data.date)
        # 当日大单数据分析.
        dd_sts = session.query(DaDanSts).filter(and_(DaDanSts.code == code, DaDanSts.date == date_str)).first()
        if dd_sts is None:
            logging.info("%s %s 涨停天数 %d, 日期: %s 无大单数据", code, name, i, str(dieting_dates))
        else:
            logging.info("%s %s 涨停天数 %d, 日期: %s 全天买入:%d, 卖出:%d, 净值:%d, 最后半小时净值:%d, 大单占市值比:%d",
                         code, name, i, str(dieting_dates),
                         dd_sts.b_volume, dd_sts.s_volume, dd_sts.net, dd_sts.lhh_net, dd_sts.ratio)
            if dd_sts.ratio >= 3 or dd_sts.net >= 5000000 or dd_sts.lhh_net >= 3000000:
                logging.info("****************** 大单加仓 %s %s *********************", code, name)
            if dd_sts.ratio <= -0.1 or dd_sts.net <= -1000000 or dd_sts.lhh_net <= -1000000:
                logging.info("****************** 注意：大单可能在抛 %s %s ***************", code, name)


def get_dieting_stocks(date_str):
    '''
    实时获取当天大单数据，不存到DB，直接内存统计并打印
    :return:
    '''

    # 取出某日期跌幅 >= 9%的股票
    hist_data = session.query(HistData).filter(
        and_(HistData.date == date_str, HistData.p_change >= RANGE)).all()

    if hist_data is None or len(hist_data) <= 0:
        logging.info("没有跌幅超过 %d 的股票", RANGE)
        return None
    logging.info("*********************** 涨停股票数量: %d", len(hist_data))
    analyze_dieting_stocks(hist_data, date_str)



if __name__ == '__main__':
    starttime = datetime.datetime.now()

    delta = datetime.timedelta(days=0)
    today = datetime.date.today()
    ndays_before = today - delta
    date_str = ndays_before.strftime('%Y-%m-%d')

    get_dieting_stocks(date_str)

    endtime = datetime.datetime.now()
    logging.info((endtime - starttime).seconds)
