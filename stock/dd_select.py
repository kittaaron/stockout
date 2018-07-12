__author__ = 'kittaaron'
# 已选大单数据

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
from model.StockInfo import StockInfo
from model.HistData import HistData

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def analyse_selected_dd():
    end_date = datetime.date.today()
    total_delta = datetime.timedelta(days=0)
    start_date = end_date - total_delta
    date_str = start_date.strftime('%Y-%m-%d')
    codes = ['000725', '000035', '000333', '000839', '000848', '000858', '002027', '601360', '601933', '300090']
    for code in codes:
        stock = session.query(StockInfo).filter(StockInfo.code == code).first()
        name = stock.name
        #logging.info('%s %s', code, date_str)
        df = ts.get_sina_dd(code, date_str)
        #logging.info(df)
        if df is None:
            logging.info("%s %s no dd", code, name)
            continue

        bvolume = 0
        svolume = 0
        lhhbvolume = 0
        lhhsvolume = 0
        for index, serie in df.iterrows():
            if serie.type == '买盘':
                bvolume += serie.volume
                if '14:30:00' < serie.time <= '14:59:59':
                    lhhbvolume += serie.volume
            if serie.type == '卖盘':
                svolume += serie.volume
                if '14:30:00' <= serie.time <= '14:59:59':
                    lhhsvolume += serie.volume

        net = (bvolume - svolume)
        lhh_net = lhhbvolume - lhhsvolume
        logging.info("%s %s %d", code, name, net)
        if net <= -1000000:
            logging.warning("%s %s 大单流出，请注意。", code, name)


if __name__ == '__main__':
    analyse_selected_dd()
