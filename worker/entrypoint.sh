#!/bin/sh
set -e

export CELERY_WORKER_MAX_TASKS=${CELERY_WORKER_MAX_TASKS:=1000}
export CELERY_QUEUES=${CELERY_QUEUES:=celery}
export C_FORCE_ROOT="true"

echo "Starting celery worker"
exec celery worker \
    -A docbleach.tasks \
    -Q ${CELERY_QUEUES} \
    --maxtasksperchild=${CELERY_WORKER_MAX_TASKS} \
    --loglevel=INFO
