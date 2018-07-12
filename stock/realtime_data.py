__author__ = 'kittaaron'
import tushare as ts
import config.logginconfig
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import dbconfig

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def dump_today_all():
    df = ts.get_today_all()
    logging.info("get today data ok.")
    df.to_sql('today_data', engine, if_exists='append')


if __name__ == '__main__':
    dump_today_all()
