import configparser
from src.slack import get_rtm_url, SlackError
import logging
from colorlog import ColoredFormatter

logger = logging.getLogger('app')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = ColoredFormatter(
    '%(log_color)s[%(levelname)s]%(reset)s %(message)s',
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

config = configparser.ConfigParser()

def run():
    config.read('/etc/slack.ini')
    slack_api_token = config['default']['slack_api_token']
    try:
        url = get_rtm_url(slack_api_token)
        logger.info('Got Slack webhook URL: {url}.'.format(url=url))
    except SlackError as error:
        logger.error(error)
        exit(1)

if __name__ == '__main__':
    run()
