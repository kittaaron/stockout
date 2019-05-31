__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductTypeConf(Base):
    __tablename__ = 'product_type_conf'

    id = Column(Integer, primary_key=True)
    # 首级目录
    parent_id = Column(Integer)
    # 二级目录
    name = Column(String)

    def __int__(self, parent_id, name):
        self.parent_id = parent_id
        self.name = name
        pass

    def __str__(self):
        msg = self.parent_id + " " + self.name
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
