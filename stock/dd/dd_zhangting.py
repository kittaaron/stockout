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
from utils import holiday_util

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()

RANGE = 9.00


def analyze_zhangting_stocks(hist_data, date_str):
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
            if date_data.p_change is None:
                continue
            if date_data.p_change >= RANGE:
                i += 1
                dieting_dates.append(date_data.date)
        # 当日大单数据分析.
        dd_sts = session.query(DaDanSts).filter(and_(DaDanSts.code == code, DaDanSts.date == date_str)).first()
        if dd_sts is None:
            logging.info("%s %s 涨停天数 %d, 日期: %s 无大单数据", code, name, i, str(dieting_dates))
        else:
            logging.info("%s %s 涨停天数 %d, 日期: %s 全天买入:%d, 卖出:%d, 净值:%d, 最后半小时买入%s,卖出%s,净值:%d, 大单占市值比:%d",
                         code, name, i, str(dieting_dates),
                         dd_sts.b_volume, dd_sts.s_volume, dd_sts.net, dd_sts.lhh_b_volume, dd_sts.lhh_s_volume, dd_sts.lhh_net, dd_sts.ratio)
            if dd_sts.ratio >= 3 or dd_sts.net >= 5000000 or dd_sts.lhh_net >= 3000000:
                logging.info("****************** 大单加仓 %s %s *********************", code, name)
            if dd_sts.ratio <= -0.1 or dd_sts.net <= -1000000 or dd_sts.lhh_net <= -1000000:
                logging.info("****************** 注意：大单可能在抛 %s %s ***************", code, name)


def analyze_next_day_info(hist_datas, next_date_str):
    codes = []
    up_num = down_num = 0
    total_change = 0
    for hist_data in hist_datas:
        codes.append(hist_data.code)
    next_day_infos = session.query(HistData).filter(
        and_(HistData.date == next_date_str, HistData.code.in_(codes))).all()
    next_day_dict = {}
    for next_day_info in next_day_infos:
        next_day_dict[next_day_info.code] = next_day_info

    for hist_data in hist_datas:
        next_day_p_change = next_day_dict[hist_data.code].p_change if hist_data.code in next_day_dict else None
        if next_day_p_change is not None:
            total_change += next_day_p_change
            if next_day_p_change > 0:
                up_num += 1
            else:
                down_num += 1
        #logging.info("%s %s %s 涨跌 %s 第二天 %s", hist_data.code, hist_data.name, hist_data.date, hist_data.p_change,
                     #next_day_p_change)
    logging.info("*********************** 汇总：%s 涨: %s, 跌 %s, 总计涨跌: %s \n", next_date_str, up_num, down_num, total_change)


def get_zhangting_stocks(date_str, next_date_str):
    '''
    实时获取当天大单数据，不存到DB，直接内存统计并打印
    :return:
    '''
    # 取出某日期跌幅 >= 9%的股票
    hist_datas = session.query(HistData).filter(
        and_(HistData.date == date_str, HistData.p_change >= RANGE)).all()

    if hist_datas is None or len(hist_datas) <= 0:
        logging.info("没有跌幅超过 %d 的股票", RANGE)
        return None
    logging.info("*********************** %s 涨停股票数量: %d", date_str, len(hist_datas))
    if next_date_str >= datetime.date.today().strftime('%Y-%m-%d'):
        for hist_data in hist_datas:
            logging.info("%s %s", hist_data.code, hist_data.name)

        codes = []
        for data in hist_datas:
            codes.append(data.code)
        sorted_dd_sts = session.query(DaDanSts).filter(
        and_(DaDanSts.code.in_(codes), DaDanSts.date == date_str)).order_by(DaDanSts.s_volume).all()
        analyze_zhangting_stocks(hist_datas, date_str)
        for dd_sts in sorted_dd_sts:
            logging.info("%s %s s_volume: %s", dd_sts.code, dd_sts.name, dd_sts.s_volume)
        return

    analyze_next_day_info(hist_datas, next_date_str)


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    hour = starttime.hour

    loop_time = 30
    delta = datetime.timedelta(days=loop_time)
    today = datetime.date.today()
    if hour <= 15:
        today -= datetime.timedelta(days=1)
    ndays_before = today - delta
    while ndays_before <= today:
        date_str = ndays_before.strftime('%Y-%m-%d')
        if holiday_util.is_holiday(date_str):
            date_str = holiday_util.get_pre_transact_date(date_str)
            ndays_before = datetime.datetime.strptime(date_str, '%Y-%m-%d')

        next_date_str = (ndays_before + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        if holiday_util.is_holiday(next_date_str):
            next_date_str = holiday_util.get_next_transact_date(next_date_str)

        get_zhangting_stocks(date_str, next_date_str)
        ndays_before = datetime.datetime.strptime(next_date_str, '%Y-%m-%d').date()

    endtime = datetime.datetime.now()
    logging.info((endtime - starttime).seconds)
