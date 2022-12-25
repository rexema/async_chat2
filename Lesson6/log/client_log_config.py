import logging
from functools import wraps


format = logging.Formatter(
    "%(asctime)s  - %(message)s ")
client_log = logging.FileHandler('client_log')
client_log.setFormatter(format)

clientlog = logging.getLogger('log')
clientlog.addHandler(client_log)
clientlog.setLevel(logging.DEBUG)


def log(func):
    @wraps(func)
    def call(*args, **kwargs):
        r = func(*args, **kwargs)
        clientlog.info(f'Функция {func.__name__} вeрнула {r}')
        clientlog.info(f'Функция {func.__name__} {func.__doc__}')
        return r

    return call


if __name__ == '__main__':
    log()
