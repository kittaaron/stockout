__author__ = 'kittaaron'
# 获取当时股票结果

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from config import dbconfig
import datetime
from model.StockInfo import StockInfo
from model.HistData import HistData

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def save(data, autocommit=True):
    session.add(data)
    if autocommit:
        session.commit()


def save_list(datas, autocommit=True):
    session.add_all(datas)
    if autocommit:
        session.commit()


def build_by_hist_data(hist_data, serie):
    hist_data.volume = serie.volume
    hist_data.open = serie.open
    hist_data.close = serie.close
    hist_data.high = serie.high
    hist_data.low = serie.low
    hist_data.p_change = serie.p_change
    hist_data.price_change = serie.price_change
    hist_data.ma5 = serie.ma5
    hist_data.ma10 = serie.ma10
    hist_data.ma20 = serie.ma20
    hist_data.v_ma5 = serie.v_ma5
    hist_data.v_ma10 = serie.v_ma10
    hist_data.v_ma20 = serie.v_ma20
    if 'turnover' in serie:
        hist_data.turnover = serie.turnover


def get_pre_day_data(code, data_str, candidate_datas):
    pass


def build_by_k_data(hist_data, serie, pre_day_data):
    '''
    :param hist_data:
    :param serie:
    :param pre_day_data:  用来计算涨跌幅<当天价减前一天收盘价>
    :return:
    '''
    hist_data.volume = serie.volume
    hist_data.open = serie.open
    hist_data.close = serie.close
    hist_data.high = serie.high
    hist_data.low = serie.low
    if pre_day_data is not None:
        price_change = round(hist_data.close - pre_day_data.close, 2)
        hist_data.price_change = price_change
        hist_data.p_change = round((price_change / pre_day_data.close) * 100, 2)


def dump_hist_data(start_date, end_date):
    stocks = session.query(StockInfo).all()

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

        i += 1
        if hist_data is not None:
            continue

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


if __name__ == '__main__':
    #dump_hist_data('2018-07-13', '2018-07-13')
    #exit(0)
    delta = datetime.timedelta(days=0)
    end_date = datetime.date.today()
    start_date = end_date - delta

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    dump_hist_data(start_date, end_date)
