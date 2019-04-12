from server.handler.BaseHandler import BaseHandler
import config.logginconfig
from stock.report.analyzer.realtime_pe_eps import *
from stock.report.analyzer.ranking import *
from stock.report.xsjj import *
import math
import logging
import config.logginconfig


class PEEPSHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        page = int(self.get_query_argument("page", '0'))
        page_size = int(self.get_query_argument("page_size", '200'))
        datas = get_pe_ranking_datas(page, page_size)
        total_row = get_total_wroe_ranking_row()
        logging.info("total_row: %s", total_row)
        total_page = math.ceil(total_row / int(page_size)) + 1
        self.write(super().return_pager_resp(list=datas, total_row=total_row, total_page=total_page))


class RankingROEHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        page = int(self.get_query_argument("page", '0'))
        page_size = int(self.get_query_argument("page_size", '200'))
        code = self.get_query_argument("code", None)
        # 筛选上市时间1、3、5、10内的
        market_time_in = self.get_query_argument("market_time_in", None)
        codes = []
        if code is not None:
            codes.append(code)
        datas = get_wroe_ranking_datas(page, page_size, codes, market_time_in)
        total_row = get_total_wroe_ranking_row()
        logging.info("total_row: %s", total_row)
        total_page = math.ceil(total_row / int(page_size)) + 1
        self.write(super().return_pager_resp(list=datas, total_row=total_row, total_page=total_page))


class NetFlowHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        page = self.get_query_argument("page", 0)
        page_size = self.get_query_argument("page_size", 200)
        datas = get_netflow_ranking_datas(page, page_size)
        self.write(super().return_json(datas))


class PBRankingHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        page = self.get_query_argument("page", 0)
        page_size = self.get_query_argument("page_size", 200)
        sort_by = self.get_query_argument("sort_by", 'pb')
        datas = get_pb_ranking_datas(page, page_size, sort_by)
        self.write(super().return_json(datas))


class XsjjHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        page = int(self.get_query_argument("page", '0'))
        page_size = int(self.get_query_argument("page_size", '200'))
        month_from = self.get_query_argument("month_from", None)
        month_to = self.get_query_argument("month_to", None)
        start_date = datetime.date.today() - relativedelta(months=+int(month_from))
        end_date = datetime.date.today() - relativedelta(months=-int(month_to))
        # 筛选上市时间1、3、5、10内的
        xsjjs = get_xsjj_by_range(page, page_size, start_date, end_date)
        xsjj_codes = []
        xsjj_time_maps = {}
        xsjj_ratio_maps = {}
        for xsjj in xsjjs:
            code = xsjj.code
            ratio = round(float(xsjj.ratio), 1)
            xsjj_codes.append(code)
            if code in xsjj_time_maps:
                oldtimeval = xsjj_time_maps[code]
                oldratioival = xsjj_ratio_maps[code]
                xsjj_time_maps[code] = oldtimeval + "," + xsjj.date
                xsjj_ratio_maps[code] = oldratioival + "," + str(ratio)
            else:
                xsjj_time_maps[code] = xsjj.date
                xsjj_ratio_maps[code] = str(xsjj.ratio)

        ranking_datas = get_wroe_ranking_datas(0, page_size, xsjj_codes)
        for ranking_data in ranking_datas:
            # 解禁时间
            if ranking_data.code in xsjj_time_maps:
                ranking_data.jjsjtime = xsjj_time_maps[ranking_data.code]
                ranking_data.jjsjratio = xsjj_ratio_maps[ranking_data.code]

        total_row = get_xsjj_totals_by_range(start_date, end_date)
        logging.info("total_row: %s", total_row)
        total_page = math.ceil(total_row / int(page_size))
        self.write(super().return_pager_resp(list=ranking_datas, total_row=total_row, total_page=total_page))


if __name__ == "__main__":
    pass
