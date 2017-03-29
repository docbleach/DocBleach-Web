from subprocess import Popen, PIPE

import tornado.gen
import tornado.web

from .base import BaseApiHandler
from ..config import PLIK_COMMAND
from ..tasks import cel
from ..utils import secure_uuid


class UploadHandler(BaseApiHandler):
    @tornado.gen.coroutine
    def post(self):
        if 'file' not in self.request.files:
            raise tornado.web.HTTPError(404)

        fileinfo = self.request.files['file']
        if type(fileinfo) == list:
            fileinfo = fileinfo[0]

        filename = str(fileinfo['filename'].strip())

        link = yield self.store_on_plik(fileinfo)
        async_res = yield self.add_task(link, filename)

        self.set_status(202)
        self.finish({'task_id': async_res.id})

    @staticmethod
    @tornado.gen.coroutine
    def store_on_plik(fileinfo):
        p = Popen(PLIK_COMMAND, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        link, err = p.communicate(input=fileinfo.body)

        if err:
            print(err)

        link = link.strip().decode('utf-8')

        return link

    @staticmethod
    @tornado.gen.coroutine
    def add_task(link, filename):
        task_id = secure_uuid()
        args = [link, filename]
        return cel.send_task('sanitize',
                             task_id=task_id,
                             # TTL for the event, equal to Plik's TTL
                             expires=3 * 3600,
                             args=args,
                             kwargs={})
