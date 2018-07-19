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


def get_real_time_quote_by_code(code):
    df = ts.get_realtime_quotes(code)
    for index, data in df.iterrows():
        return data


def get_real_time_quote_by_codes(codes):
    df = ts.get_realtime_quotes(codes)
    ret = {}
    for index, data in df.iterrows():
        ret[data.code] = data
    return ret


if __name__ == '__main__':
    get_real_time_quote_by_code('000576')
