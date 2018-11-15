__author__ = 'kittaaron'
# 获取当时股票结果

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import *
from config import dbconfig
import datetime
from model.StockInfo import StockInfo
from model.HistData import HistData
from utils.holiday_util import get_pre_transact_date
import sys
from utils.db_utils import *


def save_list(datas, autocommit=True):
    session.add_all(datas)
    if autocommit:
        session.commit()


def build_by_hist_data(hist_data, serie):
    hist_data.volume = float(serie.volume)
    hist_data.open = float(serie.open)
    hist_data.close = float(serie.close)
    hist_data.high = float(serie.high)
    hist_data.low = float(serie.low)
    hist_data.p_change = float(serie.p_change)
    hist_data.price_change = float(serie.price_change)
    hist_data.ma5 = float(serie.ma5)
    hist_data.ma10 = float(serie.ma10)
    hist_data.ma20 = float(serie.ma20)
    hist_data.v_ma5 = float(serie.v_ma5)
    hist_data.v_ma10 = float(serie.v_ma10)
    hist_data.v_ma20 = float(serie.v_ma20)
    if 'turnover' in serie:
        hist_data.turnover = float(serie.turnover)


def get_pre_day_data(code, data_str, candidate_datas):
    pass


def build_by_k_data(hist_data, serie, pre_day_data):
    '''
    :param hist_data:
    :param serie:
    :param pre_day_data:  用来计算涨跌幅<当天价减前一天收盘价>
    :return:
    '''
    hist_data.volume = float(serie.volume)
    hist_data.open = float(serie.open)
    hist_data.close = float(serie.close)
    hist_data.high = float(serie.high)
    hist_data.low = float(serie.low)
    if pre_day_data is not None:
        price_change = round(hist_data.close - pre_day_data.close, 2)
        hist_data.price_change = float(price_change)
        hist_data.p_change = round((price_change / pre_day_data.close) * 100, 2)


def dump_hist_data(start_date, end_date):
    stocks = session.query(StockInfo).all()
    # stocks = session.query(StockInfo).filter(StockInfo.code=="600682").all()

    i = 1
    for row in stocks:
        if row is None:
            continue
        # 股票代码
        code = row.code
        # code = row['code']
        # 股票名称
        name = row.name
        # name = row['name']
        logging.info("%s %s 开始处理 %d", code, name, i)

        hist_data = session.query(HistData).filter(
            and_(HistData.code == code, HistData.date >= start_date, HistData.date <= end_date)).first()

        mindatedata = session.query(HistData.code, func.min(HistData.date)).filter(HistData.code == code).group_by(
            HistData.code).first()
        maxdatedata = session.query(HistData.code, func.max(HistData.date)).filter(HistData.code == code).group_by(
            HistData.code).first()
        mindate = mindatedata[1] if mindatedata is not None else '2013-01-01'
        maxdate = maxdatedata[1] if maxdatedata is not None else datetime.date.today().strftime('%Y-%m-%d')


        i += 1
        if hist_data is not None:
            if mindate < start_date < maxdate < end_date:
                start_date = (datetime.datetime.strptime(maxdate, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime(
                    '%Y-%m-%d')
            elif start_date < mindate < end_date < maxdate:
                end_date = (datetime.datetime.strptime(mindate, '%Y-%m-%d') + datetime.timedelta(days=-1)).strftime(
                    '%Y-%m-%d')
            else:
                logging.warning("%s %s %s~%s时间段内已有数据存在", code, name, start_date, end_date)
                continue
        logging.info("开始dump %s %s %s~%s", code, name, start_date, end_date)

        df = ts.get_hist_data(code, start=start_date, end=end_date)
        stock_hist_data = []
        if df is None or df.empty is True:
            logging.info("%s %s get_hist_data 没有取到历史数据, 开始从get_k_data获取", code, name)
            df = ts.get_k_data(code, start=start_date, end=end_date)
            if df is None or df.empty is True:
                continue
            pre_day_data = None
            # 因为取出来的DataFrame正好是按时间排序的，取前一天数据时可以直接用
            for index, serie in df.iterrows():
                date = serie.date
                hist_data = HistData(code=code, name=name, date=date)
                build_by_k_data(hist_data, serie, pre_day_data)
                pre_day_data = serie
                stock_hist_data.append(hist_data)
        else:
            for index, serie in df.iterrows():
                date = index
                hist_data = HistData(code=code, name=name, date=date)
                build_by_hist_data(hist_data, serie)

                stock_hist_data.append(hist_data)
        save_list(stock_hist_data)
        logging.info("%s %s %s~%s hist data save ok", code, name, start_date, end_date)


def get_start_date():
    max_date_indb = session.query(func.max(HistData.date)).first()
    max_date_indb = max_date_indb[0] if max_date_indb is not None else "2005-12-31"

    return max_date_indb if max_date_indb == datetime.date.today().strftime('%Y-%m-%d') \
        else(datetime.datetime.strptime(max_date_indb, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')


if __name__ == '__main__':
    start_date = get_start_date()
    delta = datetime.timedelta(days=0)
    current_hour = datetime.datetime.now().hour
    today = datetime.date.today()
    end_date = today.strftime('%Y-%m-%d')
    if current_hour < 15:
        end_date = get_pre_transact_date(end_date)

    argv = len(sys.argv)
    if argv > 2:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
    logging.info("%s %s", start_date, end_date)
    dump_hist_data(start_date, end_date)
