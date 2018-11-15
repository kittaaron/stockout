__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MarketData(Base):
    __tablename__ = 'market_data'

    id = Column(Integer, primary_key=True)
    # 类型: 上市、上市A、上市B、深市、深市A 等等
    market = Column(String)
    date = Column(String)
    exchangeRate = Column(Float)
    istVol = Column(Float)
    marketValue = Column(Float)
    negotiableValue = Column(Float)
    productType = Column(Float)
    profitRate = Column(Float)
    #searchDate = Column(Float)
    trdAmt = Column(Float)
    trdTm = Column(Float)
    trdVol = Column(Float)

    def __int__(self, market, date):
        self.date = date
        self.market = market

    def __str__(self):
        msg = self.market + " " + self.market + ", date: " + str(self.date)
        return msg

    def reprJSON(self):
        return dict(market=self.market, date=self.date, exchangeRate=self.exchangeRate, istVol=self.istVol,
                    marketValue=self.marketValue, negotiableValue=self.negotiableValue, productType=self.productType,
                    profitRate=self.profitRate, trdAmt=self.trdAmt,
                    trdTm=self.trdTm, trdVol=self.trdVol)