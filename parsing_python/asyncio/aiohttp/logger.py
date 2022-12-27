import logging
import sys
from functools import wraps
import asyncio


debug_level = logging.DEBUG


def async_log(func):

    @wraps(func)
    async def logr(*args, **kwargs):
        logger.debug(f"Start{func.__name__}")
        result = await func(*args, **kwargs)
        logger.debug(f"{func.__name__} ok")
        return result
    return logr


def log(func):

    @wraps(func)
    def logr(*args, **kwargs):
        logger.debug(f"Start {func.__name__}")
        result = func(*args, **kwargs)
        logger.debug(f"{func.__name__} ok")
        return result
    return logr


# logger
logger = logging.getLogger(__file__.split("/")[-1])
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(name)s, %(funcName)s, %(levelname)s, %(asctime)s, %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(debug_level)
#