__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SteelPriceHist(Base):
    __tablename__ = 'steel_price_hist'

    id = Column(Integer, primary_key=True)
    # 股票代码
    type = Column(Integer)
    date = Column(String)
    price = Column(Integer)

    def __int__(self, type, date, price):
        self.type = type
        self.date = date
        self.price = price
        pass

    def __str__(self):
        msg = self.date + " " + self.price
        return msg

    def reprJSON(self):
        return dict(date=self.date, type=self.type, price=self.price)
