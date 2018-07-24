__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GoodStock(Base):
    __tablename__ = 'good_stock'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票代码
    name = Column(String)
    # desc
    industry_top = Column(String)
    industry_classified_top = Column(String)
    blue_chip = Column(String)
    # 1.推荐 2.关注 3.重点关注
    industry = Column(String)
    industry_classified = Column(String)
    notice = Column(String)

    def __int__(self, code, name):
        self.code = code
        self.name = name
