import logging
import sys
from functools import wraps


def logger(func):

    @wraps(func)
    def log(*args, **kwargs):
        logr.debug(f"{func} run")
        func(*args, **kwargs)
        logr.debug(f"{func} end")
    return log



# logger
logr = logging.getLogger(__file__.split("/")[-1])
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(name)s, %(funcName)s, %(levelname)s, %(asctime)s, %(message)s")
handler.setFormatter(formatter)
logr.addHandler(handler)
logr.setLevel(logging.DEBUG)
#