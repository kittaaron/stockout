__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RealTimePE(Base):
    __tablename__ = 'realtime_pe'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    pe = Column(DECIMAL)
    eps = Column(DECIMAL)
    price = Column(DECIMAL)
    date = Column(String)
    pe2 = Column(DECIMAL)
    pe3 = Column(DECIMAL)
    eps2 = Column(DECIMAL)
    eps3 = Column(DECIMAL)


    def __int__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        msg = self.code + " " + self.name
        return msg
