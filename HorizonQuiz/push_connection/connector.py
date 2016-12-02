import tornado.ioloop
import tornado.web
from django.http import JsonResponse
import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


def func_tornado(request):
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()
    return JsonResponse({'hello': 'world'})
