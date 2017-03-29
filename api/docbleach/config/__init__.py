import os

__UPLOADS__ = 'uploads/'

internal_plik_server = os.getenv('INTERNAL_PLIK_SERVER', 'https://plik.root.gg')

celery_broker = os.getenv('CELERY_BROKER')

celery_result_backend = os.getenv('CELERY_RESULT_BACKEND')

debug_mode = os.getenv('DEBUG', 'true').lower() == 'true'

advertise_server = os.getenv('DOCBLEACH_AS_SERVER_HEADER', 'false') == 'true'

PLIK_COMMAND = [
    'plik',
    '--server', internal_plik_server,
    '-t', '3h',
    '-q'
]
