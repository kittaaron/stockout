import tornado.ioloop
from tornado.web import *

from server.handler.AnalyzerHandler import *
from server.handler.ReportHandler import *
from server.handler.StockInfoHandler import StockInfoHandler
from server.handler.DDHandler import DDHandler
from server.handler.DDTopHandler import DDTopHandler
from server.handler.HistDataHandler import PriceListHandler
from server.handler.IndexHandler import IndexHandler
from server.handler.MarketDataHandler import SHMarketDataHandler,SZMarketDataHandler,SteelPriceHistHandler
from server.handler.StockAnalysisHandler import StockAnalysisHandler
from server.handler.SearchStockHandler import SearchStockHandler
from server.handler.ProductPriceHandler import ProductPriceHistHandler


class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return Application([
        (r"/static/index.html", IndexHandler),
        (r"/stock/(.*)", StockInfoHandler),
        (r"/ddtop/(.*)", DDTopHandler),
        (r"/dd/(.*)", DDHandler),
        (r"/get_market_data/sh", SHMarketDataHandler),
        (r"/get_market_data/sz", SZMarketDataHandler),
        (r"/get_steel_price_hist", SteelPriceHistHandler),
        (r"/get_ranking_pe", PEEPSHandler),
        (r"/get_ranking_wroe", RankingROEHandler),
        (r"/get_xsjj_list", XsjjHandler),
        (r"/get_report_list", ReportDetailHandler),
        (r"/get_report_chart_list", ReportDetailHandler),
        (r"/get_ranking_netflow", NetFlowHandler),
        (r"/get_ranking_pb", PBRankingHandler),
        (r"/get_price_list/(.*)", PriceListHandler),
        (r"/get_stock_analysis/(.*)", StockAnalysisHandler),
        (r"/get_stock/(.*)", SearchStockHandler),
        (r"/get_product_price_list", ProductPriceHistHandler),
    ],
        #static_path=os.path.join(os.path.dirname(__file__), "../static/js", "../static/css", "../static/fonts",
                                 #"../static/images", "../static/scss", "../static/vendors", "../static/partials"),
        #template_path=os.path.join(os.path.dirname(__file__), "../static", "../static/pages"),
        static_path=os.path.join(os.path.dirname(__file__), "../static/"),
        #template_path=os.path.join(os.path.dirname(__file__), "../static"),
        xsrf_cookies=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()