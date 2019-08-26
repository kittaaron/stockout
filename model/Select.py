__author__ = 'kittaaron'

from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Select(Base):
    __tablename__ = 'select'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)

    safe_pe = Column(Integer)

    fair_pe = Column(Integer)

    danger_pe = Column(Integer)

    predict_net = Column(Integer)

    dividend = Column(DECIMAL)

    dividend_year = Column(String)
    # 股票名称
    cc = Column(Integer)

    inc_years = Column(Integer)

    inc_rate = Column(Integer)

    inc_perpetual = Column(Integer)

    def __str__(self):
        msg = self.code + " " + self.name
        return msg