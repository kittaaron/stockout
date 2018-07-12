__author__ = 'kittaaron'
# 大单数据分析,需要先执行dd_dump.py，把当天数据导入，就可以分析了

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from config import dbconfig
import datetime
from model.StockInfo import StockInfo
from model.DaDan import DaDan
from model.DaDanSts import DaDanSts

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def get_top_dd_sts(date_str):
    top100 = session.query(DaDanSts).filter(DaDanSts.date == date_str).order_by(desc(DaDanSts.net)).limit(100).all()
    llhtop300 = session.query(DaDanSts).filter(DaDanSts.date == date_str).order_by(desc(DaDanSts.lhh_net)).limit(300).all()
    ratiotop100 = session.query(DaDanSts).filter(DaDanSts.date == date_str).order_by(desc(DaDanSts.ratio)).limit(100).all()

    lhhtop300_codes = []
    for lhhdata in llhtop300:
        lhhtop300_codes.append(lhhdata.code)

    index = 0
    for data in top100:
        index += 1
        llh_index = -1
        try:
            llh_index = lhhtop300_codes.index(data.code)
        except ValueError as err:
            pass

        if llh_index >= 0:
            logging.info("%s %s 总数据排名: %d, 最后半小时排名: %d, %s", data.code, data.name, index, llh_index + 1, data)
        else:
            logging.info("%s %s 总数据排名: %d, 最后半小时未排进前300", data.code, data.name, index)

    i2 = 1
    for data in ratiotop100:
        logging.info("大单占比排名第%d %s %s", i2, data.code, data.name)
        i2 += 1


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    get_top_dd_sts('2018-07-11')
    endtime = datetime.datetime.now()
    logging.info((endtime - starttime).seconds)
