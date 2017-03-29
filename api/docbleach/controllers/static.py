import tornado.web

from .base import BaseHandler


class StaticFileHandler(tornado.web.StaticFileHandler, BaseHandler):
    pass
