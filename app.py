from src.slack import fetch_from_slack, SlackError
from src.clients import SlackClientProtocol
from src.logs import create_logger
from src.utils import parse_url, get_config
import asyncio
import logging

from autobahn.asyncio.websocket import WebSocketClientFactory

@asyncio.coroutine
def setup():
    try:
        body = yield from fetch_from_slack('rtm.start')
    except SlackError as error:
        logger.error(error)
        return
    else:
        url = body.get('url')
        logger.info('Got Slack webhook URL: {url}.'.format(url=url))

    return url

def run():
    loop = asyncio.get_event_loop()
    url = loop.run_until_complete(setup())

    if not url:
        return

    connect = parse_url(url)

    factory = WebSocketClientFactory(url, debug=False)
    factory.protocol = SlackClientProtocol

    coro = loop.create_connection(
        factory,
        host=connect.host,
        port=connect.port,
        ssl=connect.ssl
    )
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    create_logger()
    logger = logging.getLogger('app')
    run()
