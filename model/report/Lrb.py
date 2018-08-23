__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()


class Lrb(Base):
    __tablename__ = 'lrb'

    id = Column(Integer, primary_key=True)

    code = Column(String)

    name = Column(String)

    date = Column(String)

    revenue = Column(DECIMAL)

    interest_revenue = Column(DECIMAL)

    other_revenue = Column(DECIMAL)

    oper_cost = Column(DECIMAL)

    sales_expense = Column(DECIMAL)

    manage_expense = Column(DECIMAL)

    finalcial_expense = Column(DECIMAL)

    asset_derease = Column(DECIMAL)

    fair_val_change_income = Column(DECIMAL)

    invest_income = Column(DECIMAL)

    oper_profit = Column(DECIMAL)

    non_biz_income = Column(DECIMAL)

    non_biz_expense = Column(DECIMAL)

    profit = Column(DECIMAL)

    tax = Column(DECIMAL)

    net_profit = Column(DECIMAL)

    net_profit_t_p = Column(DECIMAL)

    net_profit_b_m = Column(DECIMAL)

    minority_equity = Column(DECIMAL)

    eps = Column(DECIMAL)

    dilute_eps = Column(DECIMAL)

    def __init__(self, code, name, date):
        self.code = code
        self.name = name
        self.date = date

    def __str__(self):
        msg = "code:" + self.code + ",name: " + self.name
        return msg

    class StockInfoEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__

    def reprJSON(self):
        return dict(code=self.code, name=self.name)
