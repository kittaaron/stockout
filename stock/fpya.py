__author__ = 'kittaaron'
# 分配预案

import tushare as ts
import config.logginconfig
import logging
from config import dbconfig
from model.Fpya import Fpya
from utils.db_utils import *
from sqlalchemy import *

session = getSession()


def get_fpya():
    logging.info("开始dump数据")
    df = ts.profit_data(top=4000, year=2018)

    for index, serie in df.iterrows():
        code = serie['code']
        name = serie['name']
        year = serie['year']
        report_date = serie['report_date']
        divi = serie['divi']
        shares = serie['shares']
        old_data = session.query(Fpya).filter(
            and_(Fpya.code == code, Fpya.year == year, Fpya.report_date == report_date)).first()
        if old_data is not None:
            logging.info("%s %s %s %s 分配预案数据已存在", code, name, year, report_date)
            continue
        else:
            old_data = Fpya(code=code, name=name, year=year, report_date=report_date)
            old_data.divi = divi
            old_data.shares = shares
            logging.info("dump分配预案: %s %s %s %s %s %s ", code, name, year, report_date, divi, shares)
        session.add(old_data)
    #df.to_sql('fpya', engine, if_exists='replace', index=False, index_label='code')
    logging.info("dump成功")


if __name__ == '__main__':
    get_fpya()