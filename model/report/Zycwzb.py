__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class Zycwzb(Base):
    __tablename__ = 'zycwzb'

    id = Column(Integer, primary_key=True)

    code = Column(String)

    name = Column(String)

    date = Column(String)

    eps = Column(DECIMAL)

    bvps = Column(DECIMAL)

    epcf = Column(DECIMAL)

    por = Column(DECIMAL)

    pop = Column(DECIMAL)

    profit = Column(DECIMAL)

    invest_income = Column(DECIMAL)

    non_op_income = Column(DECIMAL)

    total_profit = Column(DECIMAL)

    net_profit = Column(DECIMAL)

    npad = Column(DECIMAL)

    cffoa = Column(DECIMAL)

    niicce = Column(DECIMAL)

    total_assets = Column(DECIMAL)

    flow_assets = Column(DECIMAL)

    total_debts = Column(DECIMAL)

    flow_debts = Column(DECIMAL)

    sheq = Column(DECIMAL)

    wroe = Column(DECIMAL)

    net_yoy = Column(DECIMAL)

    por_yoy = Column(DECIMAL)

    pop_yoy = Column(DECIMAL)

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