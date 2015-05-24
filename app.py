import tornado.ioloop
from tornado.options import (
    define,
    options,
    parse_config_file,
    parse_command_line
)
import tornado.gen as gen
import tornado.escape
from tornado.options import Error as ParseError
from tornado.websocket import websocket_connect
from tornado.httpclient import (
    AsyncHTTPClient,
    HTTPRequest,
    HTTPError
)
from src.slack import get_rtm_url, SlackError
import logging

define('port', default=5555, help='server runs on this port', type=int)
define('dev', default=False, help='sets the dev toggle', type=bool)
define('conf', default='/etc/slack.conf', help='The conf file', type=str)
define('slack_api_token', default=None, help='The slack token', type=str)


def run():
    try:
        parse_config_file(options.conf)
    except FileNotFoundError as error:
        logging.error(
            'Conf file not found. Location: {conf}'
            .format(conf=options.conf)
        )
        exit(1)
    except SyntaxError as error:
        logging.error(
            'There is an error with your conf syntax: {error}'
            .format(error=error)
        )
        exit(1)
    except ParseError as error:
        logging.error(
            'Incorrect types in you conf file: {error}'
            .format(error=error)
        )
        exit(1)

    parse_command_line()

    try:
        url = get_rtm_url(options.slack_api_token)
        logging.info('Got Slack webhook URL: {url}.'.format(url=url))
    except SlackError as error:
        logging.error(error)
        exit(1)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run()
