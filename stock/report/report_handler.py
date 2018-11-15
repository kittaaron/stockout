# encoding:utf-8

import config.logginconfig
import logging
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from config import dbconfig
import pandas as pd
from model.report.Zycwzb import Zycwzb
from model.report.Zcfzb import Zcfzb
from model.report.Cwbbzy import Cwbbzy
from model.report.Lrb import Lrb
from model.report.Xjllb import Xjllb
from model.StockInfo import StockInfo
from utils.db_utils import *


def save(data, autocommit=True):
    session.add(data)
    if autocommit:
        session.commit()


def save_all(datas, autocommit=True):
    session.add_all(datas)
    if autocommit:
        session.commit()


def build_zycwzb_obj(obj, val):
    obj.eps = val[1] if val[1] != '--' else 0
    obj.bvps = val[2] if val[2] != '--' else 0
    obj.epcf = val[3] if val[3] != '--' else 0
    obj.por = val[4] if val[4] != '--' else 0
    obj.pop = val[5] if val[5] != '--' else 0
    obj.profit = val[6] if val[6] != '--' else 0
    obj.invest_income = val[7] if val[7] != '--' else 0
    obj.non_op_income = val[8] if val[8] != '--' else 0
    obj.total_profit = val[9] if val[9] != '--' else 0
    obj.net_profit = val[10] if val[10] != '--' else 0
    obj.npad = val[11] if val[11] != '--' else 0
    obj.cffoa = val[12] if val[12] != '--' else 0
    obj.niicce = val[13] if val[13] != '--' else 0
    obj.total_assets = val[14] if val[14] != '--' else 0
    obj.flow_assets = val[15] if val[15] != '--' else 0
    obj.total_debts = val[16] if val[16] != '--' else 0
    obj.flow_debts = val[17] if val[17] != '--' else 0
    obj.sheq = val[18] if val[18] != '--' else 0
    obj.wroe = val[19] if val[19] != '--' else 0


def handle_zycwzb(code, name):
    """
    主要账务指标
    :param obj:
    :param val:
    :return:
    """
    logging.info("开始处理主要财务指标表 %s %s", code, name)
    filepath = "/Users/kittaaron/Downloads/report/" + code + "/zycwzb.csv"
    try:
        df = pd.read_csv(filepath, header=None, sep=',', encoding='gbk')
        records = []
        for index, val in df.iteritems():
            if index == 0:
                continue
            if val[0] is None or str(val[0]) == 'nan':
                continue
            date = val[0]

            # 如果code_date已经录入，则已经插入过，不继续插入
            zycwzb = session.query(Zycwzb).filter(and_(Zycwzb.code == code, Zycwzb.date == val[0])).first()
            if zycwzb is not None:
                continue

            obj = Zycwzb(code=code, name=name, date=date)
            build_zycwzb_obj(obj, val)
            records.append(obj)

        save_all(records)
    except Exception as e:
        logging.error("%s", e)
        return


def build_zcfzb_obj(obj, val):
    obj.moneytory_funds = val[1] if val[1] != '--' else 0
    obj.note_receivable = val[6] if val[6] != '--' else 0
    obj.cash_receivable = val[7] if val[7] != '--' else 0
    obj.ats = val[8] if val[8] != '--' else 0
    obj.interest_receivable = val[12] if val[12] != '--' else 0
    obj.other_receivables = val[14] if val[14] != '--' else 0
    obj.inventories = val[20] if val[20] != '--' else 0
    obj.prepaid_expence = val[21] if val[21] != '--' else 0
    obj.oca = val[24] if val[24] != '--' else 0
    obj.tca = val[25] if val[25] != '--' else 0
    obj.fixed_assets_cost = val[33] if val[33] != '--' else 0
    obj.acc_depre = val[34] if val[34] != '--' else 0
    obj.fixed_assets_disposal = val[36] if val[36] != '--' else 0
    obj.fixed_assets = val[37] if val[37] != '--' else 0
    obj.cig = val[38] if val[38] != '--' else 0
    obj.intan_assets = val[44] if val[44] != '--' else 0
    obj.shangyu = val[46] if val[46] != '--' else 0
    obj.deferred_taxes = val[49] if val[49] != '--' else 0
    obj.total_n_c_a = val[51] if val[51] != '--' else 0
    obj.total_assets = val[52] if val[52] != '--' else 0
    obj.short_term_loans = val[53] if val[53] != '--' else 0
    obj.notes_payable = val[59] if val[59] != '--' else 0
    obj.accounts_payable = val[60] if val[60] != '--' else 0
    obj.a_f_c = val[61] if val[61] != '--' else 0
    obj.total_current_liabi = val[84] if val[84] != '--' else 0
    obj.total_not_current_liabi = val[93] if val[93] != '--' else 0
    obj.total_liabi = val[94] if val[94] != '--' else 0
    obj.paid_in_capital = val[95] if val[95] != '--' else 0
    obj.capital_reserve = val[96] if val[96] != '--' else 0
    obj.capital_surplus = val[99] if val[99] != '--' else 0
    obj.un_dis_profit = val[102] if val[102] != '--' else 0
    obj.b_p_c_sh_eq = val[105] if val[105] != '--' else 0
    obj.minor_equity = val[106] if val[106] != '--' else 0
    obj.sh_eq = val[107] if val[107] != '--' else 0
    obj.sheq_liabi_sum = val[108] if val[108] != '--' else 0


def handle_zcfzb(code, name):
    """
    资产负债表
    :param obj:
    :param val:
    :return:
    """
    logging.info("开始处理资产负债表 %s %s", code, name)
    filepath = "/Users/kittaaron/Downloads/report/" + code + "/zcfzb.csv"
    try:
        df = pd.read_csv(filepath, header=None, sep=',', encoding='gbk')

        records = []
        for index, val in df.iteritems():
            if index == 0:
                continue
            if val[0] is None or str(val[0]) == 'nan':
                continue
            date = val[0]

            # 如果code_date已经录入，则已经插入过，不继续插入
            zcfzb = session.query(Zcfzb).filter(and_(Zcfzb.code == code, Zcfzb.date == val[0])).first()
            if zcfzb is not None:
                continue

            obj = Zcfzb(code=code, name=name, date=date)
            build_zcfzb_obj(obj, val)
            records.append(obj)
        save_all(records)
    except Exception as e:
        logging.error("%s", e)
        return


def is_num(val):
    try:
        if type(eval(val)) == int or type(eval(val)) == float:
            return True
        else:
            return False
    except Exception as e:
        return False


def build_cwbbzy_obj(obj, val):
    obj.revenue = val[1] if is_num(val[1]) else 0
    obj.oper_cost = val[2] if is_num(val[2]) else 0
    obj.oper_income = val[3] if is_num(val[3]) else 0
    obj.profit_before_tax = val[4] if is_num(val[4]) else 0
    obj.income_tax = val[5] if is_num(val[5]) else 0
    obj.net_profit = val[6] if is_num(val[6]) else 0
    obj.eps = val[7] if is_num(val[7]) else 0
    obj.moneytory_funds = val[8] if is_num(val[8]) else 0
    obj.cash_receivable = val[9] if is_num(val[9]) else 0
    obj.inventories = val[10] if is_num(val[10]) else 0
    obj.tca = val[11] if is_num(val[11]) else 0
    obj.fixed_assets = val[12] if is_num(val[12]) else 0
    obj.total_assets = val[13] if is_num(val[13]) else 0
    obj.total_current_liabi = val[14] if is_num(val[14]) else 0
    obj.total_not_current_liabi = val[15] if is_num(val[15]) else 0
    obj.total_liabi = val[16] if is_num(val[16]) else 0
    obj.sh_eq = val[17] if is_num(val[17]) else 0
    obj.oper_balance = val[18] if is_num(val[18]) else 0
    obj.net_cash_f_oper = val[19] if is_num(val[19]) else 0
    obj.net_cash_f_invest = val[20] if is_num(val[20]) else 0
    obj.net_cash_f_finance = val[21] if is_num(val[21]) else 0
    obj.net_increase = val[22] if is_num(val[22]) else 0
    obj.closing_balance = val[23] if is_num(val[23]) else 0


def handle_cwbbzy(code, name):
    logging.info("开始处理财务报表摘要 %s %s", code, name)
    filepath = "/Users/kittaaron/Downloads/report/" + code + "/cwbbzy.csv"
    try:
        df = pd.read_csv(filepath, header=None, sep=',', encoding='gbk')

        records = []
        for index, val in df.iteritems():
            if index == 0:
                continue
            if val[0] is None or str(val[0]) == 'nan':
                continue
            date = val[0]

            # 如果code_date已经录入，则已经插入过，不继续插入
            cwbbzy = session.query(Cwbbzy).filter(and_(Cwbbzy.code == code, Cwbbzy.date == val[0])).first()
            if cwbbzy is not None:
                continue

            obj = Cwbbzy(code=code, name=name, date=date)
            build_cwbbzy_obj(obj, val)
            records.append(obj)
        save_all(records)
    except Exception as e:
        logging.error("%s", e)
        return


def build_lrb_obj(obj, val):
    obj.revenue = val[1] if is_num(val[1]) else 0
    obj.interest_revenue = val[3] if is_num(val[3]) else 0
    obj.other_revenue = val[7] if is_num(val[7]) else 0
    obj.oper_cost = val[8] if is_num(val[8]) else 0
    obj.sales_expense = val[21] if is_num(val[21]) else 0
    obj.manage_expense = val[22] if is_num(val[22]) else 0
    obj.finalcial_expense = val[23] if is_num(val[23]) else 0
    obj.asset_derease = val[24] if is_num(val[24]) else 0
    obj.fair_val_change_income = val[25] if is_num(val[25]) else 0
    obj.invest_income = val[26] if is_num(val[26]) else 0
    obj.oper_profit = val[33] if is_num(val[33]) else 0
    obj.non_biz_income = val[34] if is_num(val[34]) else 0
    obj.non_biz_expense = val[35] if is_num(val[35]) else 0
    obj.profit = val[37] if is_num(val[37]) else 0
    obj.tax = val[38] if is_num(val[38]) else 0
    obj.net_profit = val[40] if is_num(val[40]) else 0
    obj.net_profit_t_p = val[41] if is_num(val[41]) else 0
    obj.net_profit_b_m = val[42] if is_num(val[42]) else 0
    obj.minority_equity = val[43] if is_num(val[43]) else 0
    obj.eps = val[44] if is_num(val[44]) else 0
    obj.dilute_eps = val[45] if is_num(val[45]) else 0


def handle_lrb(code, name):
    logging.info("开始处理利润表 %s %s", code, name)
    filepath = "/Users/kittaaron/Downloads/report/" + code + "/lrb.csv"
    try:
        df = pd.read_csv(filepath, header=None, sep=',', encoding='gbk')

        records = []
        for index, val in df.iteritems():
            if index == 0:
                continue
            if val[0] is None or str(val[0]) == 'nan':
                continue
            date = val[0]

            # 如果code_date已经录入，则已经插入过，不继续插入
            cwbbzy = session.query(Lrb).filter(and_(Lrb.code == code, Lrb.date == val[0])).first()
            if cwbbzy is not None:
                continue

            obj = Lrb(code=code, name=name, date=date)
            build_lrb_obj(obj, val)
            records.append(obj)
        save_all(records)
    except Exception as e:
        logging.error("%s", e)
        return


def build_xjllb_obj(obj, val):
    obj.cash_receive_f_s_s = val[1] if is_num(val[1]) else 0
    obj.deposit_increase = val[2] if is_num(val[2]) else 0
    obj.cash_in_oper = val[14] if is_num(val[14]) else 0
    obj.cash_paid_f_g_s = val[15] if is_num(val[15]) else 0
    obj.cash_paid_f_w_e = val[21] if is_num(val[21]) else 0
    obj.cash_out_oper = val[24] if is_num(val[24]) else 0
    obj.cash_net_oper = val[25] if is_num(val[25]) else 0
    obj.cash_reveive_f_i_r = val[27] if is_num(val[27]) else 0
    obj.cash_in_investment = val[32] if is_num(val[32]) else 0
    obj.cash_paid_f_f_i_l = val[33] if is_num(val[33]) else 0
    obj.cash_paid_f_investment = val[34] if is_num(val[34]) else 0
    obj.cash_receive_f_sub = val[36] if is_num(val[36]) else 0
    obj.cash_out_investment = val[39] if is_num(val[39]) else 0
    obj.cash_net_investment = val[40] if is_num(val[40]) else 0
    obj.cash_in_finance = val[46] if is_num(val[46]) else 0
    obj.cash_out_finance = val[51] if is_num(val[51]) else 0
    obj.cash_net_finance = val[52] if is_num(val[52]) else 0
    obj.net_incre_cash_equi = val[54] if is_num(val[54]) else 0
    obj.cash_equi_beginning = val[55] if is_num(val[55]) else 0
    obj.cash_equi_end = val[56] if is_num(val[56]) else 0
    obj.net = val[57] if is_num(val[57]) else 0
    obj.minority_interest = val[58] if is_num(val[58]) else 0
    obj.financial_cost = val[71] if is_num(val[71]) else 0
    obj.investment_losses = val[72] if is_num(val[72]) else 0
    obj.inventories_decre = val[75] if is_num(val[75]) else 0
    obj.others = val[81] if is_num(val[81]) else 0
    obj.cash_end = val[85] if is_num(val[85]) else 0
    obj.cash_beginning = val[86] if is_num(val[86]) else 0
    obj.cash_equi_incre = val[89] if is_num(val[89]) else 0


def handle_xjllb(code, name):
    logging.info("开始现金流量表 %s %s", code, name)
    filepath = "/Users/kittaaron/Downloads/report/" + code + "/xjllb.csv"
    try:
        df = pd.read_csv(filepath, header=None, sep=',', encoding='gbk')

        records = []
        for index, val in df.iteritems():
            if index == 0:
                continue
            if val[0] is None or str(val[0]) == 'nan':
                continue
            date = val[0]

            # 如果code_date已经录入，则已经插入过，不继续插入
            xjllb = session.query(Xjllb).filter(and_(Xjllb.code == code, Xjllb.date == val[0])).first()
            if xjllb is not None:
                continue

            obj = Xjllb(code=code, name=name, date=date)
            build_xjllb_obj(obj, val)
            records.append(obj)
        save_all(records)
    except Exception as e:
        logging.error("%s", e)
        return


if __name__ == '__main__':
    stocks = session.query(StockInfo).all()
    #stocks = session.query(StockInfo).filter(StockInfo.code == '002236').all()
    for row in stocks:
        if row is None:
            continue
        code = row.code
        name = row.name
        handle_zycwzb(code, name)
        handle_zcfzb(code, name)
        handle_cwbbzy(code, name)
        handle_lrb(code, name)
        handle_xjllb(code, name)
