import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from config import dbconfig
from model.StockInfo import StockInfo
from model.HistData import HistData
from stock.report import risk
from stock.realtime.realtime_data import get_real_time_quote_by_codes
import datetime
from utils.SMSUtil import sendMsg
from utils.db_utils import *


def analyze_codes_dd(codes, date_str, need_alert = False):
    """
    按股票代码和日期分析股票大单
    :param codes:
    :param date_str:
    :return:
    """
    real_time_datas = get_real_time_quote_by_codes(codes)
    avg_p_change = 0
    exclude_i = 0
    for code in codes:
        risk.risk_warning(code)
        stock = session.query(StockInfo).filter(StockInfo.code == code).first()
        name = stock.name
        df = ts.get_sina_dd(code, date_str)

        p_change = None
        price = None
        serie = real_time_datas[code]
        if code in real_time_datas:
            price = float(serie.price)
            pre_close = float(serie.pre_close)
            p_change = round((price - pre_close) / pre_close * 100, 2)
            if p_change != -100:
                avg_p_change += p_change
            else:
                exclude_i += 1

        if df is None:
            logging.info("%s %s no dd, 当前价: %s 涨跌 %s", code, name, price, p_change)
            continue

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
        ratio = round(net / (stock.totals*1000000) , 5)
        if net <= -1000000:
            logging.info("%s %s %d 点比:%s 当前价 %s 实时涨跌 %s. 大单流出请注意 ------------ \n", code, name, net, ratio, price, p_change)
            if need_alert:
                sendMsg(code + " dadan out, please attention.")
        else:
            logging.info("%s %s %d 点比:%s 当前价 %s 实时涨跌 %s\n", code, name, net, ratio, price, p_change)
    logging.info("股票数量: %s 平均涨跌: %s", len(codes), avg_p_change / (len(codes) - exclude_i))


def analyze_hist(codes, start_date_str, end_date_str):
    total_avg = 0
    total_codes = 0
    for code in codes:
        avg_p_change = 0
        hist_datas = session.query(HistData).filter(and_(HistData.code == code,
                                                         HistData.date <= end_date_str,
                                                         HistData.date >= start_date_str)).all()
        name = None
        if len(hist_datas) <= 0:
            logging.warning("%s %s 没找到历史数据", code, name)
            continue
        total_codes += 1
        for data in hist_datas:
            if data.p_change is None:
                logging.warning("%s %s %s p_change is None", code, name, data.date)
                continue
            avg_p_change += data.p_change
            if name is None:
                name = data.name
        total_avg += avg_p_change
        logging.info("%s %s %s~%s 天数: %s 涨跌: %s", code, name, start_date_str, end_date_str, len(hist_datas), avg_p_change)
    logging.info("平均涨跌: %s", round(total_avg/total_codes, 2))
