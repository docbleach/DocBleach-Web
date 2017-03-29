import os
import time
from subprocess import PIPE, Popen

from celery import Celery

external_plik_server = os.getenv('EXTERNAL_PLIK_SERVER', 'https://plik.root.gg')

cel = Celery(
    'docbleach',
    broker=os.getenv('CELERY_BROKER'),
    backend=os.getenv('CELERY_RESULT_BACKEND')
)

cel.config_from_object('docbleach.celeryconfig')


def get_docbleach_command(original_uri):
    return ['java',
            '-jar', 'docbleach.jar',
            '-batch',
            '-in', original_uri,
            '-out', '-'
            ]


def get_plik_command(original_filename):
    return ['plik',
            '-q',
            '--server', external_plik_server,
            '-t', '12h',
            '-n', original_filename
            ]


@cel.task(name="sanitize")
def sanitize_task(original_uri, original_filename):
    time.sleep(5)
    docbleach_command = get_docbleach_command(original_uri)
    plik_command = get_plik_command(original_filename)

    p1 = Popen(docbleach_command, stdout=PIPE, stderr=PIPE)
    p2 = Popen(plik_command, stdin=p1.stdout, stdout=PIPE)

    plik_link, plik_err = p2.communicate()
    _, docbleach_output = p1.communicate()

    # We build a "pretty" output to be displayed
    total_output = ""
    if docbleach_output:
        total_output += docbleach_output.decode('utf-8').strip()
        if plik_err:
            total_output += "\n"

    if plik_err:
        total_output += 'SEVERE ' + plik_err.decode('utf-8').strip()

    if p1.returncode == 0 and p2.returncode == 0:
        return {
            'output': total_output,
            'exit_code': 0,
            'final_file': plik_link.decode('utf-8').strip()
        }

    # return_code is the first non null exit code
    return_code = p1.returncode or p2.returncode

    return {
        'exit_code': return_code,
        'output': total_output
    }
