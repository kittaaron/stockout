from server.handler.BaseHandler import BaseHandler
import config.logginconfig
from stock.report.analyzer.realtime_pe_eps import *
from stock.report.analyzer.ranking import *
from stock.report.report_utils import *


class ReportDetailHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        page = 0
        pageSize = 10
        code = self.get_argument('code', None)
        if code is None:
            self.write(super().return_json(None))
            return
        start_date = '2007-01-31'
        end_date = get_latest_record_date()
        datas = get_reports_detail(code, start_date, end_date)

        self.write(super().return_json(datas))


class ReportChartHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        page = 0
        pageSize = 10
        code = self.get_argument('code', None)
        if code is None:
            self.write(super().return_json(None))
            return
        start_date = '2009-12-31'
        end_date = get_latest_record_date()
        datas = get_reports_detail(code, start_date, end_date)

        self.write(super().return_json(datas))


if __name__ == "__main__":
    pass
