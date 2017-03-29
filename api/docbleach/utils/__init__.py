import os
import random
import string


def secure_uuid():
    """
    Strength: 6*3 random characters from a list of 62, approx. 64^18 possible
    strings, or 2^100. Should be enough to prevent a successful bruteforce, as
    download links are only valid for 3 hours
    :return:
    """
    return id_generator() + "-" + id_generator() + "-" + id_generator()


def id_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def static(*args):
    return os.path.join('static', *args)
