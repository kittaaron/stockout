from typing import Any, Union

import tushare as ts
import logging
import config.logginconfig
from stock.report.report_utils import *
from utils.db_utils import *
from model.report.Zycwzb import Zycwzb
from sqlalchemy import *
from model.StockInfo import StockInfo
from model.RealTimePEEPS import RealTimePEEPS
from stock.report.report_utils import *
from numpy import *
from model.Buffett import Buffett


def get_codes(stocks):
    codes = []
    for stock in stocks:
        codes.append(stock.code)
    return codes


def build_map(realtimepeeps):
    ret = {}
    for realtimepeeps in realtimepeeps:
        ret[realtimepeeps.code] = realtimepeeps
    return ret

def get_stocks_map(stocks):
    ret = {}
    for stock in stocks:
        ret[stock.code] = stock
    return ret


def get_buffetts_map(buffetts):
    ret = {}
    for buffett in buffetts:
        ret[buffett.code] = buffett
    return ret


def get_pe_ranking_datas(page, pageSize):
    """
        获取根据pe排名的股票数据
    :return:
    """
    page = 0 if not page else page
    pageSize = 10 if not pageSize else pageSize
    offset = page * pageSize
    realtime_pe_eps = session.query(RealTimePEEPS).filter(and_(RealTimePEEPS.koufei_pe > 0, RealTimePEEPS.pe1 > 0))\
        .order_by(RealTimePEEPS.koufei_pe).limit(pageSize).offset(offset).all()
    codes = get_codes(realtime_pe_eps)
    stocks = session.query(StockInfo).filter(StockInfo.code.in_(codes)).all()
    buffetts = session.query(Buffett).filter(Buffett.code.in_(codes)).all()
    codes_map = get_stocks_map(stocks)
    buffetts_map = get_buffetts_map(buffetts)
    ret = []
    for realtime_pe_ep in realtime_pe_eps:
        if realtime_pe_ep.code in codes_map:
            realtime_pe_ep.industry = codes_map[realtime_pe_ep.code].industry
            realtime_pe_ep.industry_classified = codes_map[realtime_pe_ep.code].industry_classified
            realtime_pe_ep.mktcap = round(codes_map[realtime_pe_ep.code].mktcap/10000, 2) if codes_map[realtime_pe_ep.code].mktcap else 0
        if realtime_pe_ep.code in buffetts_map:
            realtime_pe_ep.flow_sub_total = buffetts_map[realtime_pe_ep.code].flow_sub_total
            realtime_pe_ep.flow_sub_flow = buffetts_map[realtime_pe_ep.code].flow_sub_flow
        #if not (realtime_pe_ep.industry == '普钢' or realtime_pe_ep.industry == '银行' or realtime_pe_ep.industry == '特种钢'):
        ret.append(realtime_pe_ep)
    logging.info("ret cnt: %s", len(ret))
    return ret


def get_total_wroe_ranking_row():
    latest_record_date = get_latest_record_date()
    cnt = session.query(func.count(Zycwzb.id)).filter(and_(Zycwzb.date == latest_record_date)).scalar()
    return cnt


def get_wroe_ranking_datas(page, pageSize):
    """
        获取根据pe排名的股票数据
    :return:
    """
    page = 0 if not page else page
    pageSize = 100 if not pageSize else pageSize
    offset = page * pageSize
    latest_record_date = get_latest_record_date()
    # 获取wroe排名前100的数据
    zycwzbs = session.query(Zycwzb).filter(and_(Zycwzb.date == latest_record_date)).order_by(desc(Zycwzb.wroe)).limit(pageSize).offset(offset).all()
    codes = get_codes(zycwzbs)

    stocks = session.query(StockInfo).filter(StockInfo.code.in_(codes)).all()
    stocks_map = get_stocks_map(stocks)

    realtimepeepss = session.query(RealTimePEEPS).filter(RealTimePEEPS.code.in_(codes)).all()
    realtimepeeps_map = build_map(realtimepeepss)

    ret = []
    for zycwzb in zycwzbs:
        code = zycwzb.code
        name = zycwzb.name
        logging.info("%s %s wroe: %s", code, name, zycwzb.wroe)
        zycwzb.price = realtimepeeps_map[code].price
        zycwzb.eps = realtimepeeps_map[code].eps1
        zycwzb.pe = realtimepeeps_map[code].pe1
        zycwzb.lastyear_pe = realtimepeeps_map[code].pe2
        zycwzb.koufei_pe = realtimepeeps_map[code].koufei_pe
        zycwzb.net_assets = round((zycwzb.total_assets - zycwzb.total_debts)/10000, 2)
        zycwzb.industry = stocks_map[code].industry
        zycwzb.variance = round(abs(zycwzb.net_profit - zycwzb.npad) / zycwzb.net_profit, 2) if zycwzb.net_profit != 0 else 0
        zycwzb.mktcap = round(stocks_map[code].mktcap / 10000, 2)
        zycwzb.predict_pe = realtimepeeps_map[code].predict_pe if realtimepeeps_map[code].predict_pe else 0
        zycwzb.predict_price = round(zycwzb.eps * zycwzb.predict_pe, 2)

        if zycwzb.variance > 0.25 or zycwzb.pe >= 25 or zycwzb.koufei_pe >= 25 or zycwzb.industry == '普钢' \
                or zycwzb.industry == '水泥' or zycwzb.industry == '化工原料':
            continue
        else:
            ret.append(zycwzb)
    logging.info("return cnt: %s", len(ret))

    return ret


def get_netflow_ranking_datas(page, pageSize):
    """
        获取根据pe排名的股票数据
    :return:
    """
    page = 0 if not page else page
    pageSize = 100 if not pageSize else pageSize
    offset = page * pageSize
    latest_record_date = get_latest_record_date()
    # 获取wroe排名前100的数据
    buffets = session.query(Buffett).order_by(desc(Buffett.flow_sub_total)).limit(pageSize).offset(offset).all()
    codes = get_codes(buffets)

    stocks = session.query(StockInfo).filter(StockInfo.code.in_(codes)).all()
    stocks_map = get_stocks_map(stocks)

    realtimepeepss = session.query(RealTimePEEPS).filter(RealTimePEEPS.code.in_(codes)).all()
    realtimepeeps_map = build_map(realtimepeepss)

    zycwzbs = session.query(Zycwzb).filter(Zycwzb.code.in_(codes)).all()
    zycwzbs_map = build_map(zycwzbs)

    ret = []
    for buffet in buffets:
        code = buffet.code
        name = buffet.name
        logging.info("%s %s", code, name)
        buffet.industry = stocks_map[code].industry
        buffet.mktcap = round(stocks_map[code].mktcap / 10000, 2)
        buffet.price = realtimepeeps_map[code].price
        buffet.pe = realtimepeeps_map[code].pe1
        buffet.koufei_pe = realtimepeeps_map[code].koufei_pe
        buffet.eps = realtimepeeps_map[code].eps1
        buffet.wroe = zycwzbs_map[code].wroe

        ret.append(buffet)
    logging.info("return cnt: %s", len(ret))

    return ret


def get_reports_detail(code, start_date, end_date):
    start_date = start_date if start_date else '2009-12-31'
    end_date = end_date if end_date else get_latest_record_date()
    realtimepeepss = session.query(Zycwzb).filter(and_(Zycwzb.code == code,
                                                       Zycwzb.date >= start_date,
                                                       Zycwzb.date <= end_date)).order_by(desc(Zycwzb.date)).all()
    return realtimepeepss


if __name__ == '__main__':
    pass
