import tornado.web

from ..config import advertise_server

CSP_POLICY = "default-src 'self' https:;" + \
             "style-src 'self' 'unsafe-inline' https:;" + \
             "img-src 'self' data: https:;" + \
             "frame-ancestors 'none';" + \
             "form-action *;"

REFERRER_POLICY = 'no-referrer, strict-origin-when-cross-origin'


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        super(BaseHandler, self).set_default_headers()

        if advertise_server:
            self.set_header('Server', 'DocBleach')
        else:
            self.clear_header('Server')

        self.set_header('X-Frame-Options', 'DENY')
        self.set_header('Referrer-Policy', REFERRER_POLICY)
        self.set_header('Content-Security-Policy', CSP_POLICY)
        self.set_header('X-Content-Type-Options', 'nosniff')
        self.set_header('X-XSS-Protection', '1; mode=block')


class BaseApiHandler(BaseHandler):
    def set_default_headers(self):
        super(BaseApiHandler, self).set_default_headers()
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

    def write_error(self, status_code, **kwargs):
        if status_code in [500, 503]:
            self.write('Error %s' % status_code)
