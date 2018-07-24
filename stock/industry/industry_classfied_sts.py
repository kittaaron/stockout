__author__ = 'kittaaron'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import text
import tushare as ts
from model.StockInfo import StockInfo
from model.GoodStock import GoodStock
from model.report.ReportData import ReportData
import logging
from config.dbconfig import getConfig
import config.logginconfig
from stock import idx
import datetime
import string
from stock.industry import industry_sts

engine = create_engine(getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def add(stock, autocommit=True):
    session.add(stock)
    if autocommit:
        session.commit()


def get_industry_classified_list():
    i_c_list = session.query(StockInfo.industry_classified).filter(StockInfo.industry_classified != '').group_by(
        StockInfo.industry_classified).all()
    ret = []
    for data in i_c_list:
        ret.append(data[0])
    return ret


def get_avg_pe_by_industry_classified():
    ret = {}
    list = session.query(StockInfo.industry_classified, func.avg(StockInfo.pe)).filter(and_(StockInfo.industry_classified != '',
                                         StockInfo.pe > 0)).group_by(StockInfo.industry_classified).all()
    for data in list:
        ret[data[0]] = round(data[1], 2)
    return ret


def save_industry_classified_top(stockinfo, rank):
    old = session.query(GoodStock).filter(GoodStock.code == stockinfo.code).first()
    if old is None:
        old = GoodStock(code=stockinfo.code, name=stockinfo.name)
    # 重点关注
    old.industry_classified_top = "龙头排名" + str(rank)
    old.industry_classified = stockinfo.industry_classified
    add(old)


def save_blue_chip(stockinfo, blue_chip_flag):
    old = session.query(GoodStock).filter(GoodStock.code == stockinfo.code).first()
    if old is None:
        old = GoodStock(code=stockinfo.code, name=stockinfo.name)
    if old.blue_chip == '蓝筹' and blue_chip_flag != 1:
        # 之前是蓝筹，现在不是
        old.notice = '之前是蓝筹,现在不是了'
    # 推荐股票
    if blue_chip_flag == 1:
        old.blue_chip = "蓝筹"
    elif blue_chip_flag == 0:
        old.blue_chip = ''
    elif blue_chip_flag == -1:
        #old.blue_chip = "蓝筹"
        if old.notice is None:
            old.notice = ''
        if old.notice.find('财报信息不全') < 0:
            old.notice += '财报信息不全'
    old.industry_classified = stockinfo.industry_classified
    add(old)


def sts_pe_by_industry_classified(industry_classified_list):
    avg_pes = get_avg_pe_by_industry_classified()
    for industry_classified in industry_classified_list:
        top10 = session.query(StockInfo).filter(and_(StockInfo.industry_classified == industry_classified,
                                                     StockInfo.pe > 0)).order_by(StockInfo.pe).limit(10).all()
        mktcaptop10 = session.query(StockInfo).filter(and_(StockInfo.industry_classified == industry_classified,
                                                           StockInfo.mktcap > 0)).order_by(
            desc(StockInfo.mktcap)).limit(10).all()
        logging.info("行业: %s 平均市盈率: %s", industry_classified, avg_pes[industry_classified])
        i = j = 0
        seta = setb = []

        last_year = datetime.date.today().year - 1
        last_two_year = last_year - 1
        last_three_year = last_two_year - 1
        last_four_year = last_three_year - 1
        last_five_year = last_four_year - 1

        top10reports = industry_sts.get_codes_reports(industry_sts.get_codes(top10), [last_year, last_two_year, last_three_year, last_four_year, last_five_year])
        mktcaptop10reports = industry_sts.get_codes_reports(industry_sts.get_codes(mktcaptop10), [last_year, last_two_year, last_three_year, last_four_year, last_five_year])
        for stockinfo in top10:
            i += 1
            code = stockinfo.code
            code_reports = top10reports[code]
            blue_chip_flag = industry_sts.is_blue_chip(stockinfo, code_reports)
            if blue_chip_flag:
                save_blue_chip(stockinfo, blue_chip_flag)
            logging.info("排名: %s %s %s %s 收入同比 %s 利润同比 %s", i, stockinfo.code, stockinfo.name, stockinfo.pe,
                         stockinfo.rev, stockinfo.profit)
            logging.info("%s 主业收入增长 %6s     净利润增长 %6s     净利同比 %6s     roe %6s     分配 %10s",
                         last_year, code_reports[last_year].mbrg, code_reports[last_year].nprg,
                         code_reports[last_year].profits_yoy, code_reports[last_year].roe, code_reports[last_year].distrib)
            logging.info("%s 主业收入增长 %6s     净利润增长 %6s     净利同比 %6s     roe %6s     分配 %10s",
                         last_two_year, code_reports[last_two_year].mbrg, code_reports[last_two_year].nprg,
                         code_reports[last_two_year].profits_yoy, code_reports[last_two_year].roe, code_reports[last_two_year].distrib)
            logging.info("%s 主业收入增长 %6s     净利润增长 %6s     净利同比 %6s     roe %6s     分配 %10s",
                         last_three_year, code_reports[last_three_year].mbrg, code_reports[last_three_year].nprg,
                         code_reports[last_three_year].profits_yoy, code_reports[last_three_year].roe, code_reports[last_three_year].distrib)
            logging.info("%s 主业收入增长 %6s     净利润增长 %6s     净利同比 %6s     roe %6s     分配 %10s",
                         last_four_year, code_reports[last_four_year].mbrg, code_reports[last_four_year].nprg,
                         code_reports[last_four_year].profits_yoy, code_reports[last_four_year].roe, code_reports[last_four_year].distrib)
            logging.info("%s 主业收入增长 %6s     净利润增长 %6s     净利同比 %6s     roe %6s     分配 %10s",
                         last_five_year, code_reports[last_five_year].mbrg, code_reports[last_five_year].nprg,
                         code_reports[last_five_year].profits_yoy, code_reports[last_five_year].roe, code_reports[last_five_year].distrib)
            seta.append(stockinfo.code + " " + stockinfo.name)
        for stockinfo in mktcaptop10:
            j += 1
            if j <= 3:
                save_industry_classified_top(stockinfo, j)
            code = stockinfo.code
            code_reports = mktcaptop10reports[code]
            blue_chip_flag = industry_sts.is_blue_chip(stockinfo, code_reports)
            if blue_chip_flag:
                save_blue_chip(stockinfo, blue_chip_flag)
            logging.info("市值: %s %s %s %s pe: %s 收入同比 %s 利润同比 %s", j, stockinfo.code, stockinfo.name, stockinfo.mktcap,
                         stockinfo.pe, stockinfo.rev, stockinfo.profit)
            logging.info("%s 主业收入增长 %6s     净利润增长 %6s     净利同比 %6s     roe %6s     分配 %6s",
                         last_year, code_reports[last_year].mbrg, code_reports[last_year].nprg,
                         code_reports[last_year].profits_yoy, code_reports[last_year].roe, code_reports[last_year].distrib)
            logging.info("%s 主业收入增长 %6s     净利润增长 %6s     净利同比 %6s     roe %6s     分配 %6s",
                         last_two_year, code_reports[last_two_year].mbrg, code_reports[last_two_year].nprg,
                         code_reports[last_two_year].profits_yoy, code_reports[last_two_year].roe, code_reports[last_two_year].distrib)
            logging.info("%s 主业收入增长 %6s     净利润增长 %6s     净利同比 %6s     roe %6s     分配 %6s",
                         last_three_year, code_reports[last_three_year].mbrg, code_reports[last_three_year].nprg,
                         code_reports[last_three_year].profits_yoy, code_reports[last_three_year].roe, code_reports[last_three_year].distrib)
            logging.info("%s 主业收入增长 %6s     净利润增长 %6s     净利同比 %6s     roe %6s     分配 %6s",
                         last_four_year, code_reports[last_four_year].mbrg, code_reports[last_four_year].nprg,
                         code_reports[last_four_year].profits_yoy, code_reports[last_four_year].roe, code_reports[last_four_year].distrib)
            logging.info("%s 主业收入增长 %6s     净利润增长 %6s     净利同比 %6s     roe %6s     分配 %6s",
                         last_five_year, code_reports[last_five_year].mbrg, code_reports[last_five_year].nprg,
                         code_reports[last_five_year].profits_yoy, code_reports[last_five_year].roe, code_reports[last_five_year].distrib)
            seta.append(stockinfo.code + " " + stockinfo.name)
            setb.append(stockinfo.code + " " + stockinfo.name)
        logging.info(list(set(seta).intersection(set(setb))))
        logging.info("--------------------------------------------------------------------------------------")


def stock_analysis_by_industry_classified():
    industry_classified_list = get_industry_classified_list()
    sts_pe_by_industry_classified(industry_classified_list)


if __name__ == '__main__':
    stock_analysis_by_industry_classified()
