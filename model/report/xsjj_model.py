__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class xsjj_model(Base):
    __tablename__ = 'xsjj'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    date = Column(String)

    count = Column(DECIMAL)
    ratio = Column(DECIMAL)

    def __int__(self, code, name, date):
        self.code = code
        self.name = name
        self.date = date

    def __str__(self):
        msg = self.code + " " + self.name + " " + str(self.date) + ",解禁数量: " + str(self.count) + \
              ",占总股数: " + str(self.ratio)
        return msg
