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
from utils.db_utils import *


def get_industry_list():
    i_c_list = session.query(StockInfo.industry).filter(StockInfo.industry != '').group_by(
        StockInfo.industry).all()
    ret = []
    for data in i_c_list:
        ret.append(data[0])
    return ret


def get_concept_classified_dict():
    ccdf = ts.get_concept_classified()
    concept_classified_dict = ccdf.to_dict(orient='records')
    ret = {}
    for data in concept_classified_dict:
        ret[data['code']] = data['c_name']
    return ret


def get_codes(stocks):
    codes = []
    for stock in stocks:
        codes.append(stock.code)
    return codes


def get_codes_reports(codes, years):
    """
    获取年报(第4季度报表)
    :param codes:
    :param years:
    :return:
    """
    if len(codes) <= 0 or len(years) <= 0:
        return None

    ret = {}
    for code in codes:
        ret[code] = {}
        for year in years:
            ret[code][year] = ReportData()
    reports = session.query(ReportData).filter(and_(ReportData.code.in_(codes),
                                                    ReportData.year.in_(years), ReportData.season == 4)).all()
    for report in reports:
        code = report.code
        year = report.year
        if code not in ret:
            ret[code] = {}
        ret[code][year] = report
    return ret


def get_avg_pe_by_industry():
    ret = {}
    list = session.query(StockInfo.industry, func.avg(StockInfo.pe)).filter(and_(StockInfo.industry != '',
                                         StockInfo.pe > 0)).group_by(StockInfo.industry).all()
    for data in list:
        ret[data[0]] = round(data[1], 2)
    return ret


def save_industry_top(stockinfo, rank):
    old = session.query(GoodStock).filter(GoodStock.code == stockinfo.code).first()
    if old is None:
        old = GoodStock(code=stockinfo.code, name=stockinfo.name)
    # 重点关注
    old.industry_top = "龙头排名" + str(rank)
    old.industry = stockinfo.industry
    save(old)


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
    old.industry = stockinfo.industry
    add(old)


def is_blue_chip(stockinfo, last_five_years_reports):
    """
    如果股票最近几年收入一直增长、利润一直为正：则股票不会太差；
    如果股票的利润率也一直增长，则股票
    :param stockinfo:
    :param last_five_years_reports:
    :return:  -1 信息缺少没法准确判断 1 是蓝筹 0不是
    """
    current_ok = True
    if stockinfo.pe > 0 and stockinfo.rev > 0 and stockinfo.profit > 0:
        pass
    else:
        current_ok = False
    report_ok = True
    info_lack = False
    reports = sorted(last_five_years_reports.items(), key=lambda r: r[0], reverse=True)
    lack_i = 0
    current_year = datetime.date.today().year
    for data in reports:
        if data is None:
            continue
        year = data[0]
        report = data[1]
        if report is None:
            logging.warning("%s %s %s财报信息不全", stockinfo.code, stockinfo.name, year)
            info_lack = True
            continue
        if (report.mbrg is not None and report.mbrg < 0) or \
                report.nprg is not None and report.nprg < 0 or \
                report.profits_yoy is not None and report.profits_yoy < 0:
            logging.warning("%s %s %s 数据不好", stockinfo.code, stockinfo.name, year)
            report_ok = False
            break
        else:
            report_ok = True
    if info_lack:
        return -1

    if current_ok and report_ok:
        logging.info("%s %s 是蓝筹", stockinfo.code, stockinfo.name)
    return 1 if current_ok and report_ok else 0


def sts_pe_by_industry(industry_list):
    avg_pes = get_avg_pe_by_industry()
    for industry in industry_list:
        top10 = session.query(StockInfo).filter(and_(StockInfo.industry == industry,
                                                     StockInfo.pe > 0)).order_by(StockInfo.pe).limit(10).all()
        mktcaptop10 = session.query(StockInfo).filter(and_(StockInfo.industry == industry,
                                                           StockInfo.mktcap > 0)).order_by(
            desc(StockInfo.mktcap)).limit(10).all()
        logging.info("行业: %s 平均市盈率: %s", industry, avg_pes[industry])
        i = j = 0
        seta = setb = []

        last_year = datetime.date.today().year - 1
        last_two_year = last_year - 1
        last_three_year = last_two_year - 1
        last_four_year = last_three_year - 1
        last_five_year = last_four_year - 1

        top10reports = get_codes_reports(get_codes(top10), [last_year, last_two_year, last_three_year, last_four_year, last_five_year])
        mktcaptop10reports = get_codes_reports(get_codes(mktcaptop10), [last_year, last_two_year, last_three_year, last_four_year, last_five_year])
        for stockinfo in top10:
            i += 1
            code = stockinfo.code
            code_reports = top10reports[code]
            blue_chip_flag = is_blue_chip(stockinfo, code_reports)
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
                save_industry_top(stockinfo, j)
            code = stockinfo.code
            code_reports = mktcaptop10reports[code]
            blue_chip_flag = is_blue_chip(stockinfo, code_reports)
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


def stock_analysis_by_industry():
    industry_list = get_industry_list()
    sts_pe_by_industry(industry_list)


if __name__ == '__main__':
    stock_analysis_by_industry()
