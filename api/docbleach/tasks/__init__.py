from celery import Celery

from ..config import celery_broker, celery_result_backend

cel = Celery(
    'docbleach',
    broker=celery_broker,
    backend=celery_result_backend
)
