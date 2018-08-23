__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()


class Xjllb(Base):
    __tablename__ = 'xjllb'

    id = Column(Integer, primary_key=True)

    code = Column(String)

    name = Column(String)

    date = Column(String)

    cash_receive_f_s_s = Column(DECIMAL)

    deposit_increase = Column(DECIMAL)

    cash_in_oper = Column(DECIMAL)

    cash_paid_f_g_s = Column(DECIMAL)

    cash_paid_f_w_e = Column(DECIMAL)

    cash_out_oper = Column(DECIMAL)

    cash_net_oper = Column(DECIMAL)

    cash_reveive_f_i_r = Column(DECIMAL)

    cash_in_investment = Column(DECIMAL)

    cash_paid_f_f_i_l = Column(DECIMAL)

    cash_paid_f_investment = Column(DECIMAL)

    cash_receive_f_sub = Column(DECIMAL)

    cash_out_investment = Column(DECIMAL)

    cash_net_investment = Column(DECIMAL)

    cash_in_finance = Column(DECIMAL)

    cash_out_finance = Column(DECIMAL)

    cash_net_finance = Column(DECIMAL)

    net_incre_cash_equi = Column(DECIMAL)

    cash_equi_beginning = Column(DECIMAL)

    cash_equi_end = Column(DECIMAL)

    net = Column(DECIMAL)

    minority_interest = Column(DECIMAL)

    financial_cost = Column(DECIMAL)

    investment_losses = Column(DECIMAL)

    inventories_decre = Column(DECIMAL)

    others = Column(DECIMAL)

    cash_end = Column(DECIMAL)

    cash_beginning = Column(DECIMAL)

    cash_equi_incre = Column(DECIMAL)


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
