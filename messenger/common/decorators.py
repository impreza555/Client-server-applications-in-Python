import inspect
import logging
import sys
sys.path.append('../')
import traceback
from log import client_log_config
from log import server_log_config


def log(func):
    def log_saver(*args, **kwargs):
        logger = 'server' if 'server.py' in sys.argv[0] else 'client'
        logger = logging.getLogger(logger)
        res = func(*args, **kwargs)
        logger.debug(f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func.__module__}.'
                     f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     f'Вызов из функции {inspect.stack()[1][3]}')
        return res
    return log_saver


def loger(decorator):
    def wrapper(cls):
        getattribute = cls.__getattribute__

        def newattribute(cls, name):
            attr = getattribute(cls, name)
            return decorator(attr)
        cls.__getattribute__ = newattribute
        return cls
    return wrapper
