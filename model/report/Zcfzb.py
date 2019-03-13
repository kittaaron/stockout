__author__ = 'kittaaron'
from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class Zcfzb(Base):
    __tablename__ = 'zcfzb'

    id = Column(Integer, primary_key=True)

    code = Column(String)

    name = Column(String)

    date = Column(String)

    moneytory_funds = Column(DECIMAL)

    note_receivable = Column(DECIMAL)

    cash_receivable = Column(DECIMAL)

    ats = Column(DECIMAL)

    interest_receivable = Column(DECIMAL)

    other_receivables = Column(DECIMAL)

    inventories = Column(DECIMAL)

    prepaid_expence = Column(DECIMAL)

    oca = Column(DECIMAL)

    tca = Column(DECIMAL)

    fixed_assets = Column(DECIMAL)

    fixed_assets_cost = Column(DECIMAL)

    acc_depre = Column(DECIMAL)

    cig = Column(DECIMAL)

    intan_assets = Column(DECIMAL)

    fixed_assets_disposal = Column(DECIMAL)

    shangyu = Column(DECIMAL)

    deferred_taxes = Column(DECIMAL)

    total_assets = Column(DECIMAL)

    total_n_c_a = Column(DECIMAL)

    short_term_loans = Column(DECIMAL)

    notes_payable = Column(DECIMAL)

    accounts_payable = Column(DECIMAL)

    a_f_c = Column(DECIMAL)

    total_liabi = Column(DECIMAL)

    total_current_liabi = Column(DECIMAL)

    total_not_current_liabi = Column(DECIMAL)

    liab_ratio = Column(DECIMAL)

    non_current_liab_ratio = Column(DECIMAL)

    paid_in_capital = Column(DECIMAL)

    capital_reserve = Column(DECIMAL)

    capital_surplus = Column(DECIMAL)

    un_dis_profit = Column(DECIMAL)

    b_p_c_sh_eq = Column(DECIMAL)

    minor_equity = Column(DECIMAL)

    sh_eq = Column(DECIMAL)

    sheq_liabi_sum = Column(DECIMAL)

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