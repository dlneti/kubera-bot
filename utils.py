import logging
from datetime import datetime

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
        timestamp /= 1000

    return datetime.fromtimestamp(timestamp)

# print(convert_timestamp([datetime.timestamp(datetime.now()) for i in range(10)]))