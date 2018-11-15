import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("index.html", name="aaron")