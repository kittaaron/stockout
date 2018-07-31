import tornado.ioloop
from tornado.web import *
from server.handler.StockInfoHandler import StockInfoHandler


class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return Application([
        (r"/", MainHandler),
        (r"/stock/(.*)", StockInfoHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()