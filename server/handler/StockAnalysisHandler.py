import tornado.ioloop
from server.handler.BaseHandler import BaseHandler
from stock.report.report_query import *


class StockAnalysisHandler(BaseHandler):
    def get(self, code):
        # 获取最近一次年报的指标
        zbs = {}
        zycwzb = get_latest_year_zycwzb(code)
        zcfzb = get_latest_year_zcfzb(code)
        zbs['zycwzb'] = zycwzb
        zbs['zcfzb'] = zcfzb
        # 赢利指标
        zbs['profit_idx_score'] = self.get_profit_idx_score(zycwzb)
        # 增长指标
        zbs['growth_idx_score'] = self.get_growth_idx_score(zycwzb)
        # 偿债指标
        zbs['solvency_idx_score'] = self.get_solvency_idx_score(zcfzb)
        # 现金流指标
        zbs['cashflow_idx_score'] = self.get_cashflow_idx_score(zycwzb)
        # 商誉
        zbs['willbill_ratio_score'] = self.get_willbill_ratio_score(zcfzb)
        # 总资产周转率
        zbs['total_assets_turnover_score'] = self.get_total_assets_turnover_score(zycwzb)
        # 资产负债率
        zbs['debt_ratio_score'] = self.get_debt_ratio_score(zycwzb)
        self.write(super().return_json(zbs))

    def get_profit_idx_score(self, zycwzb):
        score = 5
        if zycwzb.wroe <= 0:
            score = 5
        elif 0 <= zycwzb.wroe <= 5:
            score = 30
        elif 5 <= zycwzb.wroe <= 10:
            score = 50
        elif 10 <= zycwzb.wroe <= 15:
            score = 60
        elif 15 <= zycwzb.wroe <= 20:
            score = 70
        elif 20 <= zycwzb.wroe <= 25:
            score = 80
        elif 25 <= zycwzb.wroe <= 35:
            score = 90
        elif 35 < zycwzb.wroe:
            score = 99
        return score

    def get_growth_idx_score(self, zycwzb):
        # 增长率得分
        score = 5
        if zycwzb.profit_yoy < 0:
            score = 5
        elif 0 <= zycwzb.profit_yoy <= 1.05:
            # 增长5%
            score = 50
        elif 1.05 < zycwzb.profit_yoy <= 1.08:
            score = 60
        elif 1.08 < zycwzb.profit_yoy <= 1.10:
            score = 65
        elif 1.10 < zycwzb.profit_yoy <= 1.14:
            score = 70
        elif 1.14 < zycwzb.profit_yoy <= 1.18:
            score = 75
        elif 1.18 < zycwzb.profit_yoy <= 1.22:
            score = 80
        elif 1.22 < zycwzb.profit_yoy <= 1.25:
            score = 85
        elif 1.25 < zycwzb.profit_yoy <= 1.30:
            score = 90
        elif 1.30 < zycwzb.profit_yoy:
            score = 99
        return score

    def get_solvency_idx_score(self, zcfzb):
        # 偿债能力得分
        score = 5
        moneytory_funds = zcfzb.moneytory_funds
        short_term_loans = zcfzb.short_term_loans
        # 非流动负债
        total_not_current_liabi = zcfzb.total_not_current_liabi

        solvency_target = short_term_loans + total_not_current_liabi
        if solvency_target <= 0:
            return 99
        if moneytory_funds < 0:
            score = 5
        # 如果货币资金比短期贷款还小
        elif 0 < moneytory_funds < short_term_loans:
            if moneytory_funds/short_term_loans <= 0.8:
                score = 5
            else:
                score = 20
        # 货币资金比短期贷款多，但是比短期借款+长期负债少
        elif short_term_loans <= moneytory_funds <= solvency_target:
            score = 50
        elif moneytory_funds > solvency_target:
            if moneytory_funds / solvency_target <= 1.2:
                score = 60
            elif 1.2 <= moneytory_funds / solvency_target <= 2:
                score = 70
            elif 2 <= moneytory_funds / solvency_target <= 3:
                score = 80
            elif 3 <= moneytory_funds / solvency_target <= 10:
                score = 90
            elif 10 <= moneytory_funds / solvency_target:
                score = 99
        return score

    def get_cashflow_idx_score(self, zycwzb):
        # 现金流得分
        score = 5
        # 扣非净利
        npad = zycwzb.npad
        # 经营产生的现金流量净额
        cffoa = zycwzb.cffoa

        if cffoa <= 0 or npad <= 0:
            score = 5
        else:
            cashflow_ratio = round(cffoa / npad, 2)
            if cashflow_ratio <= 0.1:
                score = 10
            elif 0.1 <= cashflow_ratio <= 0.2:
                score = 20
            elif 0.2 <= cashflow_ratio <= 0.3:
                score = 30
            elif 0.3 <= cashflow_ratio <= 0.4:
                score = 40
            elif 0.4 <= cashflow_ratio <= 0.5:
                score = 50
            elif 0.5 <= cashflow_ratio <= 0.6:
                score = 60
            elif 0.6 <= cashflow_ratio <= 0.7:
                score = 65
            elif 0.7 <= cashflow_ratio <= 0.8:
                score = 70
            elif 0.8 <= cashflow_ratio <= 0.9:
                score = 75
            elif 0.9 <= cashflow_ratio <= 1:
                score = 80
            elif 1 <= cashflow_ratio:
                score = 90
        return score

    def get_willbill_ratio_score(self, zcfzb):
        # 偿债能力得分
        score = 5
        # 扣非净利
        willbill = zcfzb.shangyu
        # 归母净资产
        b_p_c_sh_eq = zcfzb.b_p_c_sh_eq

        ratio = round(willbill * 100 / b_p_c_sh_eq, 2)
        # 商誉占比越小越好，但是不可能为负，除非净资产负
        if ratio < 0:
            score = 5
        elif ratio <= 1:
            score = 99
        elif 1 < ratio <= 3:
            score = 95
        elif 3 < ratio <= 5:
            score = 90
        elif 5 < ratio <= 8:
            score = 85
        elif 8 < ratio <= 12:
            score = 80
        elif 12 < ratio <= 16:
            score = 75
        elif 16 < ratio <= 20:
            score = 70
        elif 20 < ratio <= 24:
            score = 65
        elif 24 < ratio <= 28:
            score = 60
        elif 28 < ratio <= 35:
            score = 50
        elif 35 < ratio <= 45:
            score = 40
        elif 45 < ratio <= 60:
            score = 20
        else:
            score = 0
        return score

    def get_total_assets_turnover(self, zycwzb):
        total_assets_turnover = round(zycwzb.por / zycwzb.total_assets, 2)
        return total_assets_turnover

    def get_total_assets_turnover_score(self, zycwzb):
        score = 0
        total_assets_turnover = round(zycwzb.por / zycwzb.total_assets, 2)
        # 一般公司总资产周转率 0.8 左右, 越大越好
        if total_assets_turnover < 0 or 0 < total_assets_turnover <= 0.1:
            return 0
        if 0.1 < total_assets_turnover <= 0.2:
            score = 10
        elif 0.2 < total_assets_turnover <= 0.3:
            score = 20
        elif 0.3 < total_assets_turnover <= 0.4:
            score = 30
        elif 0.4 < total_assets_turnover <= 0.5:
            score = 40
        elif 0.5 < total_assets_turnover <= 0.6:
            score = 50
        elif 0.6 < total_assets_turnover <= 0.7:
            score = 60
        elif 0.7 < total_assets_turnover <= 0.8:
            score = 70
        elif 0.8 < total_assets_turnover <= 1.2:
            score = 75
        elif 1.2 < total_assets_turnover <= 1.6:
            score = 85
        elif 1.6 < total_assets_turnover <= 2:
            score = 90
        elif 2 < total_assets_turnover:
            score = 95

        return score

    def get_debt_ratio(self, zycwzb):
        debt_ratio = round(zycwzb.total_debts / zycwzb.total_assets, 2)
        return debt_ratio

    def get_debt_ratio_score(self, zycwzb):
        score = 0
        debt_ratio = round(zycwzb.total_debts / zycwzb.total_assets, 2)
        if score > 0.9 or score < 0:
            return score
        if score <= 0.1:
            score = 90
        if 0.1 < score <= 0.2:
            score = 80
        if 0.2 < score <= 0.3:
            score = 75
        if 0.3 < score <= 0.4:
            score = 70
        if 0.4 < score <= 0.5:
            score = 60
        if 0.5 < score <= 0.6:
            score = 45
        if 0.6 < score <= 0.7:
            score = 35
        if 0.7 < score:
            score = 10
        return score



if __name__ == "__main__":
    pass
