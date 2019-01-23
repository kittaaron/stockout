__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HistData(Base):
    __tablename__ = 'hist_data'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    date = Column(String)
    open = Column(DECIMAL)
    high = Column(DECIMAL)
    close = Column(DECIMAL)
    low = Column(DECIMAL)
    volume = Column(DECIMAL)
    price_change = Column(DECIMAL)
    p_change = Column(DECIMAL)
    ma5 = Column(DECIMAL)
    ma10 = Column(DECIMAL)
    ma20 = Column(DECIMAL)
    v_ma5 = Column(DECIMAL)
    v_ma10 = Column(DECIMAL)
    v_ma20 = Column(DECIMAL)
    turnover = Column(DECIMAL)

    def __int__(self, code, name, date):
        self.code = code
        self.name = name
        self.date = date

    def __str__(self):
        msg = self.code + " " + self.name + ", 开盘: " + str(self.open) + ",收盘(手): " + str(self.close) + \
              ",涨跌: " + str(self.p_change) + ",换手率: " + str(self.turnover)
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
