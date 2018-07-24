__author__ = 'kittaaron'
# 机构席位追踪

import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig
import datetime

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def get_inst_tops():
    # 统计周期5、10、30和60日，默认为5日
    df = ts.inst_tops(days=5)
    df.to_sql('inst_tops', engine, if_exists='append', index=False, index_label='code')


if __name__ == '__main__':
    get_inst_tops()