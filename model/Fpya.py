__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


### 分配预案


class Fpya(Base):
    __tablename__ = 'fpya'

    id = Column(Integer, primary_key=True)
    # 股票代码
    code = Column(String)
    # 股票名称
    name = Column(String)
    year = Column(String)
    report_date = Column(String)
    divi = Column(DECIMAL)
    shares = Column(DECIMAL)

    def __int__(self, code, name, year, report_date):
        self.code = code
        self.name = name
        self.year = year
        self.report_date = report_date

    def __str__(self):
        msg = "name: " + self.name
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
