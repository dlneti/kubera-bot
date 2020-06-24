import logging
from datetime import datetime
from time import time


# wrappers

def timeit(f):
    def wrapper(*a, **kw):
        now = time()
        res = f(*a, **kw)
        print(f"Operation {f.__name__} took {time() - now} seconds")
        return res
    return wrapper
    
# logging

def setup_logging(name="", initial=False, prefix_path="", class_name=False):
    # create logger
    logger = logging.getLogger(_get_logger_name(name, prefix_path, class_name))

    if initial:
        logger.setLevel(logging.INFO)

        # create console handler and set level to INFO
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    return logger

def _get_logger_name(source, prefix_path, class_name):
    root_logger_name = "Binance_bot"
    logger_name = [root_logger_name]

    if prefix_path:
        logger_name.append(prefix_path)

    if class_name:
        logger_name.append(source.__class__.__name__)

    return ".".join(logger_name)

# misc

def convert_timestamp(timestamp):
    if isinstance(timestamp, list):
        converted = []
        for t in timestamp:
            converted.append(convert_timestamp(t))
        return converted

    # convert to integer
    timestamp = int(timestamp)

    # convert to seconds from ms
    if len(str(timestamp)) == 13:
        timestamp = int(timestamp / 1000)
    
    assert (len(str(timestamp)) == 10), f"Bad timestamp! {timestamp}"

    return datetime.fromtimestamp(timestamp)

# print(convert_timestamp([datetime.timestamp(datetime.now()) for i in range(10)]))


def from_sc_to_human(msg: str) -> str:
    """Converts snkce_case to Human readable

    Args:
        msg (str): snakce_case string

    Returns:
        str: converted
    """
    chunks = msg.split("_")
    if len(chunks) == 1:
        return chunks[0].capitalize()
    
    return " ".join(chunks).capitalize()
    