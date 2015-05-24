import logging
from colorlog import ColoredFormatter


def create_logger():
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        '%(log_color)s[%(levelname)-8s]%(reset)s %(purple)s%(filename)s/%(funcName)s/%(lineno)d%(reset)s %(message)s',
        datefmt=None,
        reset=True,
        log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'white,bg_red',
        },
        secondary_log_colors={},
        style='%'
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
