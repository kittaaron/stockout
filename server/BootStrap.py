import tornado.ioloop
from tornado.web import *
from server.handler.StockInfoHandler import StockInfoHandler
from server.handler.DDHandler import DDHandler
from server.handler.DDTopHandler import DDTopHandler
from server.handler.IndexHandler import *
from server.handler.MarketDataHandler import *


class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return Application([
        (r"/static/index.html", IndexHandler),
        #(r"/", MainHandler),
        (r"/stock/(.*)", StockInfoHandler),
        (r"/ddtop/(.*)", DDTopHandler),
        (r"/dd/(.*)", DDHandler),
        (r"/get_market_data/sh", SHMarketDataHandler),
        (r"/get_market_data/sz", SZMarketDataHandler),
        (r"/get_steel_price_hist", SteelPriceHistHandler),
    ],
        #static_path=os.path.join(os.path.dirname(__file__), "../static/js", "../static/css", "../static/fonts",
                                 #"../static/images", "../static/scss", "../static/vendors", "../static/partials"),
        #template_path=os.path.join(os.path.dirname(__file__), "../static", "../static/pages"),
        static_path=os.path.join(os.path.dirname(__file__), "../static"),
        #template_path=os.path.join(os.path.dirname(__file__), "../static"),
        xsrf_cookies=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()