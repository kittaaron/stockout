__author__ = 'kittaaron'
import tushare as ts
import config.logginconfig
import logging
from config import dbconfig
from utils.db_utils import *


def get_sz50s():
    df = ts.get_sz50s()
    if df is None:
        logging.info("get sz50 return none.")
        return {}
    records_dict = df.to_dict(orient='records')
    ret = {}
    for data in records_dict:
        ret[data['code']] = data['name']
    return ret


def get_zz500s():
    df = ts.get_zz500s()
    if df is None:
        logging.info("get zz500 return none.")
        return {}
    records_dict = df.to_dict(orient='records')
    ret = {}
    for data in records_dict:
        ret[data['code']] = data['name']
    return ret


def dump_index():
    df = ts.get_index()
    df.to_sql('index_data', engine, if_exists='append', index = False, index_label = 'code')


if __name__ == '__main__':
    dump_index()
    #get_zz500s()
