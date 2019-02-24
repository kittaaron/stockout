__author__ = 'kittaaron'
# 获取当时股票结果

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import *
from config import dbconfig
from stock.basic import *
import datetime
from model.StockInfo import StockInfo
from model.HistData import HistData
from utils.holiday_util import get_pre_transact_date
import sys
from utils.db_utils import *
from model.report.Zycwzb import Zycwzb
from stock.report.report_utils import *


session = getSession()


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
    #stocks = getSession().query(StockInfo).filter(StockInfo.code == '600309').all()

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
        #logging.info("%s %s 开始处理 %d", code, name, i)

        mindatedata = session.query(HistData.code, func.min(HistData.date)).filter(HistData.code == code).group_by(
            HistData.code).first()
        maxdatedata = session.query(HistData.code, func.max(HistData.date)).filter(HistData.code == code).group_by(
            HistData.code).first()
        mindate = mindatedata[1] if mindatedata is not None else '2013-01-01'
        maxdate = maxdatedata[1] if maxdatedata is not None else datetime.date.today().strftime('%Y-%m-%d')
        logging.info("%s %s 已dump数据 %s至%s %s", code, name, mindate, maxdate, i)

        i += 1

        if mindate < start_date < maxdate < end_date or maxdate < start_date:
            start_date = (datetime.datetime.strptime(maxdate, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime(
                '%Y-%m-%d')
        elif start_date < mindate < end_date < maxdate:
            end_date = (datetime.datetime.strptime(mindate, '%Y-%m-%d') + datetime.timedelta(days=-1)).strftime(
                '%Y-%m-%d')
        elif end_date < mindate:
            pass
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
                logging.info("%s %s get_k_data 没有取到历史数据.", code, name)
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
    try:
        max_date_indb = session.query(func.max(HistData.date)).first()
        max_date_indb = max_date_indb[0] if max_date_indb is not None else "2005-12-31"

        return max_date_indb if max_date_indb == datetime.date.today().strftime('%Y-%m-%d') \
            else(datetime.datetime.strptime(max_date_indb, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    except Exception as e:
        pass
    finally:
        session.close()


def getzycwzbs_map(zycwzbs):
    ret = {}
    for zycwzb in zycwzbs:
        ret[zycwzb.date] = zycwzb
    return ret


def get_price_list(code, start_date, end_date):
    try:
        hist_data = session.query(HistData).filter(
            and_(HistData.code == code, HistData.date >= start_date, HistData.date <= end_date)).all()

        stockinfo = get_by_code(code)
        zycwzbs = session.query(Zycwzb).filter(and_(Zycwzb.code == code)).order_by(desc(Zycwzb.date)).all()
        zycwzbs_map = getzycwzbs_map(zycwzbs)
        for hist_data_i in hist_data:
            price_date = hist_data_i.date
            price = hist_data_i.close
            report_date = get_latest_record_date_by_date(price_date)
            pre_year_report_date = get_pre_yearreport_date(report_date)
            static_eps = 0
            dynamic_eps = 0
            if pre_year_report_date in zycwzbs_map:
                ## 计算前一年的净利润，再乘以增长率，得出动态市盈指标
                static_eps = round((zycwzbs_map[pre_year_report_date].net_profit / (stockinfo.totals * 10000)), 2)
            if report_date in zycwzbs_map and zycwzbs_map[report_date].net_yoy is not None:
                dynamic_eps = round(static_eps * zycwzbs_map[report_date].net_yoy, 2)
            static_pe = round(price / static_eps, 2) if static_eps != 0 else 0
            dynamic_pe = round(price / dynamic_eps, 2) if dynamic_eps != 0 else 0
            logging.info("日期: %s, report_date: %s, pre_year_report_date: %s, price: %s, 静态eps: %s, 静态pe: %s, 动态eps: %s, 动态pe: %s",
                         price_date, report_date, pre_year_report_date, price, static_eps, static_pe, dynamic_eps, dynamic_pe)
            hist_data_i.static_pe8 = round(static_eps * 8, 2)
            hist_data_i.static_pe12 = round(static_eps * 12, 2)
            hist_data_i.static_pe16 = round(static_eps * 16, 2)
            hist_data_i.static_pe20 = round(static_eps * 20, 2)
            hist_data_i.dynamic_pe8 = round(dynamic_eps * 8, 2)
            hist_data_i.dynamic_pe12 = round(dynamic_eps * 12, 2)
            hist_data_i.dynamic_pe16 = round(dynamic_eps * 16, 2)
            hist_data_i.dynamic_pe20 = round(dynamic_eps * 20, 2)
        return hist_data
    except Exception as e:
        pass
    finally:
        session.close()


if __name__ == '__main__':
    start_date = get_start_date()
    delta = datetime.timedelta(days=0)
    current_hour = datetime.datetime.now().hour
    today = datetime.date.today()
    end_date = today.strftime('%Y-%m-%d')
    if current_hour < 15:
        end_date = get_pre_transact_date(end_date)

    argv = len(sys.argv)
    start_date = '2018-12-14'
    if argv > 2:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
    if start_date > end_date:
        logging.warning("开始日期 %s 不能大于结束日期 %s", start_date, end_date)
        exit(0)
    logging.info("%s %s", start_date, end_date)
    dump_hist_data(start_date, end_date)
