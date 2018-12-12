__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Buffett(Base):
    __tablename__ = 'buffett'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    flow_sub_total = Column(DECIMAL)
    flow_sub_flow = Column(DECIMAL)
    pb = Column(DECIMAL)

    def __int__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        msg = self.code + " " + self.name
        return msg

    def reprJSON(self):
        ret = {}
        for item in self.__dict__.items():
            key = item[0]
            val = item[1]
            if key.startswith("_"):
                continue
            ret[key] = val
        return ret
