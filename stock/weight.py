__author__ = 'kittaaron'

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import tushare as ts
from config import dbconfig
from model.StockWeight import StockWeight
import logging

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()

def save_hs300s():
    df = ts.get_hs300s()
    if df == None:
        return
    hs300s_dict = df.to_dict("orient='records'")
    for data in hs300s_dict:
        code = data['code']
        stock_weight = session.query(StockWeight).filter_by(and_(StockWeight.code==code, StockWeight.date==data['date'])).one()
        if stock_weight != None:
            continue
        else:
            logging.info("stock_weight: %s", stock_weight)
            session.add(stock_weight)


if __name__ == '__main__':
    save_hs300s()