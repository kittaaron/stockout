__author__ = 'kittaaron'

from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StockWeight(Base):
    __tablename__ = 'stockweight'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    # 股票行业
    date = Column(String)
    # 股票行业
    weight = Column(DECIMAL)

    def __str__(self):
        msg = "code:" + self.code + ",name: " + self.name + ",date: " + self.date + ",weight: " + self.weight;
        return msg