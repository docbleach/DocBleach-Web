import os
import sys
import time

from marathon import MarathonClient
from marathon import MarathonError
from redis import StrictRedis

dcos_master = os.getenv('DCOS_MASTER') or input("Enter the DNS hostname or IP of your Marathon Instance: ")
userid = os.getenv('MARATHON_USER') or input('Enter the username for the DCOS cluster: ')
password = os.getenv('MARATHON_PWD') or input('Enter the password for the DCOS cluster: ')
marathon_app = os.getenv('APP_NAME') or input("Enter the Marathon Application Name to scale (eg: /worker): ")
redis_uri = os.getenv('REDIS_URI') or input("Enter the Redis URI, including password (eg: redis://localhost:8999/2): ")
max_instances = os.getenv('MAX_INSTANCES') or 10
min_instances = os.getenv('MIN_INSTANCES') or 1

c = MarathonClient(dcos_master, username=userid, password=password)
r = StrictRedis.from_url(redis_uri)

while True:
    print("Loop!")
    app = None
    while app is None:
        try:
            app = c.get_app(marathon_app)
        except MarathonError as err:
            print(err)
            app = None
            time.sleep(1)

    waitingDocs = r.llen("celery")

    instances = app.instances

    if waitingDocs == instances:
        pass
    elif waitingDocs > instances:
        instances += 1
    else:
        instances -= 1

    instances = min(max_instances, max(min_instances, instances))
    print("App instances: ", app.instances, " - New value: ", instances)
    if app.instances != instances:
        print("Delta: ", (app.instances - instances))
        c.scale_app(marathon_app, instances=instances, force=True)
    sys.stdout.flush()
    time.sleep(2)
