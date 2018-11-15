__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

zbmcs = ['深证成指', '深证综指', '中小板指', '创业板指', '上市公司数', '上市证券数', '市场总成交金额', '股票总股本',
         '股票流通股本', '股票总市值', '股票流通市值', '股票成交金额', '平均股票价格', '股票平均市盈率', '股票平均换手率']

class MarketDataSZ(Base):
    __tablename__ = 'market_data_sz'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    zbtype = Column(Integer)

    brsz = Column(Float)
    bsrzj = Column(Float)
    fd = Column(Float)
    bnzg = Column(Float)
    zgzrq = Column(String)

    def __int__(self, date, zbtype, brsz):
        self.date = date
        self.zbtype = zbtype
        self.brsz = brsz

    def __str__(self):
        msg = self.date + " " + self.date + ", zbtype: " + str(self.zbtype) + ", brsz: " + str(self.brsz)
        return msg

    def reprJSON(self):
        return dict(date=self.date, zbtype=self.zbtype, brsz=self.brsz, bsrzj=self.bsrzj,
                    fd=self.fd, bnzg=self.bnzg, zgzrq=self.zgzrq)