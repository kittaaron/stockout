__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductHistPrice(Base):
    __tablename__ = 'product_prict_list'

    id = Column(Integer, primary_key=True)
    # 首级目录
    category0 = Column(String)
    # 二级目录
    category1 = Column(String)
    date = Column(String)
    price = Column(Float)

    def __int__(self, category0, category1, date, price):
        pass

    def __str__(self):
        msg = self.category0 + " " + self.category0 + " " + self.date + " " + self.price
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
