__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HKStock(Base):
    __tablename__ = 'hk_stock'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    date = Column(String)
    price = Column(Float)
    percent = Column(Float)

    updown = Column(Float)
    open = Column(Float)
    yestclose = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    turnover = Column(Integer)
    exchange_rate = Column(Float)
    zf = Column(Float)
    pe = Column(Float)
    fixedpe = Column(Float)
    mkt_cap = Column(Integer)
    eps = Column(Float)
    total_turnover = Column(Integer)
    net_profit = Column(Integer)

    def __int__(self, code, name, date):
        self.code = code
        self.name = name
        self.date = date

    def __str__(self):
        msg = self.code + " " + self.name
        return msg
