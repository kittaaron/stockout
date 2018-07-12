__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DaDan(Base):
    __tablename__ = 'dd'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    date = Column(String)
    time = Column(String)
    price = Column(DECIMAL)
    preprice = Column(DECIMAL)
    volume = Column(BigInteger)
    type = Column(String)

    def __int__(self, code, name, date):
        self.code = code
        self.name = name
        self.date = date

    def __str__(self):
        msg = "name: " + self.name + ",price: " + str(self.price) + ",volume(手): " + str(self.volume) + \
              ",type: " + str(self.type)
        return msg
