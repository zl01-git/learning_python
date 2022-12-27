import logging
import sys
import inspect
from program import ParsingImages


def logger(func):
    def log(*args, **kwargs):
        lgr.debug(f"{func} started")
        result = func(*args, **kwargs)
        lgr.debug(f"{result}")
        lgr.debug(f"{func} finished")
        return result
    return log


def async_logger(coro):
    async def log(*args, **kwargs):
        lgr.debug(f"{coro} started")
        result = await coro(*args, **kwargs)
        lgr.debug(f"{result}")
        lgr.debug(f"{coro} finished")
        return result
    return log


for name, func in inspect.getmembers(ParsingImages, inspect.isfunction):
    if inspect.iscoroutinefunction(func):
        setattr(ParsingImages, name, async_logger(func))
    elif inspect.isfunction(func):
        setattr(ParsingImages, name, logger(func))



# logger
lgr = logging.getLogger(__file__.split("/")[-1])
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(levelname)s, %(asctime)s, %(message)s")
handler.setFormatter(formatter)
lgr.addHandler(handler)
lgr.setLevel(logging.DEBUG)
#