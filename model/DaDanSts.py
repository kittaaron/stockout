__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DaDanSts(Base):
    __tablename__ = 'dd_sts'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    date = Column(String)
    b_volume = Column(BigInteger)
    s_volume = Column(BigInteger)
    net = Column(BigInteger)
    # 最后半小时数据
    lhh_b_volume = Column(BigInteger)
    lhh_s_volume = Column(BigInteger)
    lhh_net = Column(BigInteger)

    fhh_b_volume = Column(BigInteger)
    fhh_s_volume = Column(BigInteger)
    fhh_net = Column(BigInteger)

    ratio = Column(DECIMAL)
    lhh_ratio = Column(DECIMAL)

    def __int__(self, code, name, date):
        self.code = code
        self.name = name
        self.date = date

    def __str__(self):
        msg = self.code + " " + self.name + ",b_volume: " + str(self.b_volume) + ",s_volume(手): " + str(self.s_volume) + \
              ",net: " + str(self.net) + ",lhh_b_volume: " + str(self.lhh_b_volume) + \
              ",lhh_s_volume: " + str(self.lhh_s_volume) + ",lhh_net: " + str(self.lhh_net) + \
              ",ratio: " + str(self.ratio) + ",lhh_ratio: " + str(self.lhh_ratio)
        return msg
