import tornado.gen

from .base import BaseApiHandler
from ..tasks import cel


class TaskHandler(BaseApiHandler):
    @tornado.gen.coroutine
    def get(self, task_id):
        data = yield self.get_task_meta(task_id)
        result_data = {'result': data['result'], 'status': data['status']}

        self.finish(result_data)

    @staticmethod
    @tornado.gen.coroutine
    def get_task_meta(task_id):
        return cel.backend.get_task_meta(task_id)
