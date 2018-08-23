__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class Cwbbzy(Base):
    __tablename__ = 'cwbbzy'

    id = Column(Integer, primary_key=True)

    code = Column(String)

    name = Column(String)

    date = Column(String)

    revenue = Column(DECIMAL)

    oper_cost = Column(DECIMAL)

    oper_income = Column(DECIMAL)

    profit_before_tax = Column(DECIMAL)

    income_tax = Column(DECIMAL)

    net_profit = Column(DECIMAL)

    eps = Column(DECIMAL)

    moneytory_funds = Column(DECIMAL)

    cash_receivable = Column(DECIMAL)

    inventories = Column(DECIMAL)

    tca = Column(DECIMAL)

    fixed_assets = Column(DECIMAL)

    total_assets = Column(DECIMAL)

    total_current_liabi = Column(DECIMAL)

    total_not_current_liabi = Column(DECIMAL)

    total_liabi = Column(DECIMAL)

    sh_eq = Column(DECIMAL)

    oper_balance = Column(DECIMAL)

    net_cash_f_oper = Column(DECIMAL)

    net_cash_f_invest = Column(DECIMAL)

    net_cash_f_finance = Column(DECIMAL)

    net_increase = Column(DECIMAL)

    closing_balance = Column(DECIMAL)

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