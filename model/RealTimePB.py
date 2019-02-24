__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RealTimePB(Base):
    __tablename__ = 'realtime_pb'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    date = Column(String)
    price = Column(DECIMAL)
    total_assets = Column(DECIMAL)
    flow_assets = Column(DECIMAL)
    total_debts = Column(DECIMAL)
    net_assets = Column(DECIMAL)
    sheq = Column(DECIMAL)
    mktcap = Column(DECIMAL)
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
