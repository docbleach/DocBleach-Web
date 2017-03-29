import tornado.web
from tornado.log import enable_pretty_logging

from .config import debug_mode
from .controllers import *
from .utils import static

application = tornado.web.Application([
    (r'/static/(.*)', StaticFileHandler, {'path': static()}),
    (r'/doc/()', StaticFileHandler, {'path': static('swagger', 'index.html')}),
    (r'/doc/(.*)', StaticFileHandler, {'path': static('swagger')}),
    (r'/()', StaticFileHandler, {'path': static('index.html')}),

    (r'/ping', PingHandler),
    (r'/v1/ping', PingHandler),
    (r'/v1/tasks', UploadHandler),
    (r'/v1/tasks/(.*)', TaskHandler),
], debug=debug_mode)

enable_pretty_logging()
