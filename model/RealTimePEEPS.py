__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RealTimePEEPS(Base):
    __tablename__ = 'realtime_pe_eps'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    koufei_pe = Column(DECIMAL)
    pe1 = Column(DECIMAL)
    pe2 = Column(DECIMAL)
    pe3 = Column(DECIMAL)
    pe4 = Column(DECIMAL)
    koufei_eps = Column(DECIMAL)
    eps1 = Column(DECIMAL)
    eps2 = Column(DECIMAL)
    eps3 = Column(DECIMAL)
    eps4 = Column(DECIMAL)
    price = Column(DECIMAL)
    eval_price = Column(DECIMAL)
    eval_price_ratio = Column(DECIMAL)
    std_devi = Column(DECIMAL)

    latest_report_date = Column(String)
    date = Column(String)

    def __int__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        msg = self.code + " " + self.name
        return msg
