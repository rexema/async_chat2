import logging
from functools import wraps

format = logging.Formatter(
    "%(asctime)s -  %(message)s ")
server_log = logging.FileHandler('server_log')
server_log.setFormatter(format)

serverlog = logging.getLogger('log')
serverlog.addHandler(server_log)
serverlog.setLevel(logging.DEBUG)


def log(func):
    @wraps(func)
    def call(*args, **kwargs):
        r = func(*args, **kwargs)
        serverlog.info(f'Функция {func.__name__} вeрнула {r}')
        serverlog.info(f'Функция {func.__name__} {func.__doc__}')
        return r

    return call


if __name__ == '__main__':
    log()
