from server.handler.BaseHandler import BaseHandler
import config.logginconfig
from stock.report.analyzer.realtime_pe_eps import *
from stock.report.analyzer.ranking import *
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
        datas = get_wroe_ranking_datas(page, page_size)
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


if __name__ == "__main__":
    pass
