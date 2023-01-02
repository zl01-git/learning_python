import logging
import inspect
import sys
from program import ParsingImages


class StreamLogger:

    def sync_logger(self, func):
        def log(*args, **kwargs):
            logger.debug(f"{func.__name__}, {func}")
            result = func(*args, **kwargs)
            logger.debug(f"{result}")
            logger.debug(f"{func.__name__}")
            return result
        return log

    
    async def async_logger(self, coro):
        async def log(*args, **kwargs):
            logger.debug("start coro")
            result = await coro(*args, **kwargs)
            logger.debug(f"{result}")
            logger.debug("finish coro")
            return result
        return log




# logger
logger = logging.getLogger("logit")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(name)s, %(levelname)s, %(asctime)s, %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
#

lgr = StreamLogger()

for name, func in inspect.getmembers(ParsingImages, inspect.isfunction):
    if inspect.isfunction(func):
        setattr(ParsingImages, name, lgr.sync_logger(func))
    elif inspect.iscoroutinefunction(func):
        setattr(ParsingImages, name, lgr.async_logger(func))
