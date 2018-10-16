__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ExtraZB(Base):
    __tablename__ = 'extra_zb'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    date = Column(String)
    acid_ratio = Column(DECIMAL)
    liquidity_ratio = Column(DECIMAL)
    por_yoy = Column(DECIMAL)
    pop_yoy = Column(DECIMAL)
    net_yoy = Column(DECIMAL)


    def __int__(self, code, name, date):
        self.code = code
        self.name = name
        self.date = date

    def __str__(self):
        msg = "name: " + self.name
        return msg
