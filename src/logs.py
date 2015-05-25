import logging
from colorlog import ColoredFormatter


def create_logger():
    ''' This function abstracts the creation of the app logger.
        On initial run you create the logger and from then on,
        access it using `logger = logging.getLogger('app')`.
    '''
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()

    format = '%(log_color)s[%(levelname)-8s]%(reset)s '\
             '%(purple)s%(filename)s/%(funcName)s/%(lineno)d%(reset)s '\
             '%(message)s'

    formatter = ColoredFormatter(
        format,
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

    return
