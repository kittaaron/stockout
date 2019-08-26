__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL, Float
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()


class Fhsg(Base):
    # 分红送股
    __tablename__ = 'fhsg'

    id = Column(Integer, primary_key=True)

    code = Column(String)

    name = Column(String)

    end_date = Column(String)

    ann_date = Column(String)

    stk_div = Column(Float)

    stk_bo_rate = Column(Float)

    stk_co_rate = Column(Float)

    cash_div = Column(Float)

    cash_div_tax = Column(Float)

    record_date = Column(String)

    ex_date = Column(String)

    pay_date = Column(String)

    div_listdate = Column(String)

    imp_ann_date = Column(String)

    base_date = Column(String)

    base_share = Column(Float)

    cash_rate = Column(Float)


    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        msg = "code:" + self.code + ",name: " + self.name
        return msg

    class StockInfoEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__

    def reprJSON(self):
        return dict(code=self.code, name=self.name, end_date=self.end_date, cash_div=self.cash_div,
                    cash_div_tax=self.cash_div_tax, cash_rate=self.cash_rate, base_share=self.base_share,
                    stk_div=self.stk_div, ex_date=self.ex_date)
