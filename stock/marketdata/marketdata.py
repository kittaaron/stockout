__author__ = 'kittaaron'

from sqlalchemy import and_
from utils.db_utils import *
from model.market.MarketDataSH import MarketData
from model.market.MarketDataSZ import MarketDataSZ
from model.market.MarketDataSZ import zbmcs
from model.industry.SteelPrice import SteelPriceHist


def get_sh_market_data(market, productType, start_date, end_date):
    records = session.query(MarketData).filter(and_(MarketData.date >= start_date,
                                                   MarketData.date <= end_date,
                                                   MarketData.market == market,
                                                   MarketData.productType == productType)).order_by(MarketData.date).all()
    return records


def get_sz_market_data(zbtype, start_date, end_date):
    records = session.query(MarketDataSZ).filter(and_(MarketDataSZ.date >= start_date,
                                                      MarketDataSZ.date <= end_date,
                                                      MarketDataSZ.zbtype == zbtype)).order_by(MarketDataSZ.date).all()
    for recordI in records:
        zbtype = recordI.zbtype if recordI.zbtype else 0
        recordI.zbmc = zbmcs[int(zbtype) - 1]
    return records


def get_steel_price_hist(type, start_date, end_date):
    records = session.query(SteelPriceHist).filter(and_(SteelPriceHist.date >= start_date,
                                                        SteelPriceHist.date <= end_date,
                                                        SteelPriceHist.type == type)).order_by(SteelPriceHist.date).all()
    return records


if __name__ == '__main__':
    pass
