__author__ = 'kittaaron'

import tushare as ts
import config.logginconfig
import logging
from model.ReportData import ReportData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig
import math

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def build_report_data(report_data, data):
    report_data.code = data['code']
    report_data.name = data['name']
    if not math.isnan(data['eps']):
        report_data.eps = data['eps']
    if not math.isnan(data['eps_yoy']):
        report_data.eps_yoy = data['eps_yoy']
    if not math.isnan(data['bvps']):
        report_data.bvps = data['bvps']
    if not math.isnan(data['roe']):
        report_data.roe = data['roe']
    if not math.isnan(data['epcf']):
        report_data.epcf = data['epcf']
    if not math.isnan(data['net_profits']):
        report_data.net_profits = data['net_profits']
    if not math.isnan(data['profits_yoy']):
        report_data.profits_yoy = data['profits_yoy']
    if str(data['distrib']) == 'nan':
        report_data.distrib = '' if str(data['distrib']) == 'nan' else str(data['distrib'])
    report_data.report_date = data['report_date']


def build_profit_data(report_data, data):
    if not math.isnan(data['net_profit_ratio']):
        report_data.net_profit_ratio = data['net_profit_ratio']
    if not math.isnan(data['gross_profit_rate']):
        report_data.gross_profit_rate = data['gross_profit_rate']
    if not math.isnan(data['business_income']):
        report_data.business_income = data['business_income']
    if not math.isnan(data['bips']):
        report_data.bips = data['bips']


def build_operation_data(report_data, data):
    if not math.isnan(data['arturnover']):
        report_data.arturnover = data['arturnover']
    if not math.isnan(data['arturndays']):
        report_data.arturndays = data['arturndays']
    if not math.isnan(data['inventory_turnover']):
        report_data.inventory_turnover = data['inventory_turnover']
    if not math.isnan(data['inventory_days']):
        report_data.inventory_days = data['inventory_days']
    if not math.isnan(data['currentasset_turnover']):
        report_data.currentasset_turnover = data['currentasset_turnover']
    if not math.isnan(data['currentasset_days']):
        report_data.currentasset_days = data['currentasset_days']


def build_growth_data(report_data, data):
    if not math.isnan(data['mbrg']):
        report_data.mbrg = data['mbrg']
    if not math.isnan(data['nprg']):
        report_data.nprg = data['nprg']
    if not math.isnan(data['nav']):
        report_data.nav = data['nav']
    if not math.isnan(data['targ']):
        report_data.targ = data['targ']
    if not math.isnan(data['epsg']):
        report_data.epsg = data['epsg']
    if not math.isnan(data['seg']):
        report_data.seg = data['seg']


def build_debtpaying_data(report_data, data):
    if isfloat(data['currentratio']):
        report_data.currentratio = float(data['currentratio'])
    if isfloat(data['quickratio']):
        report_data.quickratio = float(data['quickratio'])
    if isfloat(data['cashratio']):
        report_data.cashratio = float(data['cashratio'])
    if isfloat(data['icratio']):
        report_data.icratio = float(data['icratio'])
    if isfloat(data['sheqratio']):
        report_data.sheqratio = float(data['sheqratio'])
    if isfloat(data['adratio']):
        report_data.adratio = float(data['adratio'])


def build_cashflow_data(report_data, data):
    if not math.isnan(data['cf_sales']):
        report_data.cf_sales = data['cf_sales']
    if not math.isnan(data['rateofreturn']):
        report_data.rateofreturn = data['rateofreturn']
    if not math.isnan(data['cf_nm']):
        report_data.cf_nm = data['cf_nm']
    if not math.isnan(data['cf_liabilities']):
        report_data.cf_liabilities = data['cf_liabilities']
    if not math.isnan(data['cashflowratio']):
        report_data.cashflowratio = data['cashflowratio']


def dump_report_data(year, season):
    # 业绩主表数据
    rdf = ts.get_report_data(year, season)
    logging.info("get report data ok.")
    # 盈利能力数据
    pdf = get_profit_data_dict(year, season)
    logging.info("get profit data ok.")
    # 营运能力数据
    odf = get_operation_data_dict(year, season)
    logging.info("get operation data ok.")
    # 成长能力数据
    gdf = get_growth_data_dict(year, season)
    logging.info("get growth data ok.")
    # 偿债能力数据
    ddf = get_debtpaying_data_dict(year, season)
    logging.info("get debtpaying data ok.")
    # 现金流量数据
    cdf = get_cashflow_data_dict(year, season)
    logging.info("get cashflow data ok.")
    # 盈利能力数据
    if rdf is None:
        return
    else:
        records = rdf.to_dict("records")
        i = 0
        for data in records:
            code = data['code']
            report_data = session.query(ReportData).filter_by(code=code, year=year, season=season).first()
            if report_data is None:
                report_data = ReportData()
            logging.info("build code: %s report data.", code)
            report_data.year = year
            report_data.season = season
            build_report_data(report_data, data)
            if code in pdf:
                build_profit_data(report_data, pdf[code])
            if code in odf:
                build_operation_data(report_data, odf[code])
            if code in gdf:
                build_growth_data(report_data, gdf[code])
            if code in ddf:
                build_debtpaying_data(report_data, ddf[code])
            if code in cdf:
                build_cashflow_data(report_data, cdf[code])

            i += 1
            logging.info("stat to add report data: %s, %d", report_data, i)
            add(report_data)
        logging.info("save end.")


def get_profit_data_dict(year, season):
    pdf = ts.get_profit_data(year, season)
    ret_dict = {}
    if pdf is None:
        return ret_dict
    records = pdf.to_dict("records")
    for data in records:
        ret_dict[data['code']] = data
    return ret_dict


def get_operation_data_dict(year, season):
    odf = ts.get_operation_data(year, season)
    ret_dict = {}
    if odf is None:
        return ret_dict
    records = odf.to_dict("records")
    for data in records:
        ret_dict[data['code']] = data
    return ret_dict


def get_growth_data_dict(year, season):
    gdf = ts.get_growth_data(year, season)
    ret_dict = {}
    if gdf is None:
        return ret_dict
    records = gdf.to_dict("records")
    for data in records:
        ret_dict[data['code']] = data
    return ret_dict


def get_debtpaying_data_dict(year, season):
    ddf = ts.get_debtpaying_data(year, season)
    ret_dict = {}
    if ddf is None:
        return ret_dict
    records = ddf.to_dict("records")
    for data in records:
        ret_dict[data['code']] = data
    return ret_dict


def get_cashflow_data_dict(year, season):
    cdf = ts.get_cashflow_data(year, season)
    ret_dict = {}
    if cdf is None:
        return ret_dict
    records = cdf.to_dict("records")
    for data in records:
        ret_dict[data['code']] = data
    return ret_dict


def add(report_data, autocommit=True):
    session.add(report_data)
    if autocommit:
        session.commit()


if __name__ == '__main__':
    dump_report_data(2017, 4)
