from configparser import (
    ConfigParser,
    NoSectionError,
    NoOptionError
)
import logging

from src.slack import (
    fetch_from_slack,
    SlackError,
    SlackClientProtocol
)
from src.logs import create_logger
from src.utils import parse_url
import asyncio

from autobahn.asyncio.websocket import WebSocketClientFactory


def run():
    create_logger()
    logger = logging.getLogger('app')
    file = '/etc/slack.ini'

    config = ConfigParser()
    success = config.read(file)

    if not success:
        logger.error(
            'Configuration file not found: {location}'.format(location=file)
        )
        return

    try:
        slack_api_token = config.get('slack', 'slack_api_token')
    except (NoSectionError, NoOptionError) as error:
        logger.error(
            'Error in configuration file: {error}'.format(error=error))
        return
    else:
        logger.info(
            'Loaded configuration file from: {location}'.format(location=file)
        )

    try:
        url = fetch_from_slack('rtm.start', slack_api_token).get('url')
    except SlackError as error:
        logger.error(error)
        return
    else:
        logger.info('Got Slack webhook URL: {url}.'.format(url=url))

    connect = parse_url(url)


if __name__ == '__main__':
    run()
