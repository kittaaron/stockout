__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PorYoySts(Base):
    __tablename__ = 'por_yoy_sts'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    por_grow_cnt = Column(Integer)
    por_grow_10_cnt = Column(Integer)
    por_grow_20_cnt = Column(Integer)

    def __int__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        msg = self.code + " " + self.name
        return msg
