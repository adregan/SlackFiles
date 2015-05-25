import asyncio
import aiohttp
import logging
from .utils import get_config

logger = logging.getLogger('app')

config = get_config('/etc/slack.ini')

slack_api_token = config.get('slack', 'slack_api_token')


class SlackError(Exception):
    pass


@asyncio.coroutine
def fetch_from_slack(method: str) -> dict:
    ''' This generator makes a POST request to the slack API. 
        Pass in the Slack RPC method to make the request.
        If there is any trouble coming from the Slack server
        or if the token doesn't successfully allow authorization, raises a
        SlackError. Otherwise, returns the response body.
    '''
    # Set the method and the token on the url
    url = 'https://slack.com/api/{method}'.format(method=method)

    params = {'token': slack_api_token}

    try:
        resp = yield from aiohttp.request('post', url, params=params)
    except aiohttp.errors.ClientResponseError as err:
        error = 'ClientResponseError connecting to {url}. {error}'.format(
            url=url,
            error=err
        )
        raise SlackError(error)

    if resp.status != 200:
        error = 'Couldn\'t connect to Slack API. Status code: {code}'.format(
            code=resp.status
        )
        raise SlackError(error)

    body = yield from resp.json()

    if not body.get('ok', False):
        error = 'Error authorizing with slack: {error}'.format(
            error=body.get('error')
        )
        raise SlackError(error)

    return body

class SlackClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        logger.info("Server connected: {0}".format(response.peer))

    def onOpen(self):
        logger.info("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        # The payload comes as bytes, decode before loading the JSON
        payload = json.loads(payload.decode('utf8'))

        # Only interested in the file comments
        if payload.get('type') != 'file_comment_added':
            print(payload)
            return

        # Saves a reference to these two items
        file = payload.get('file', {})
        comment = payload.get('comment', {})

        # Grab the mimetype to easily distinguish type of file
        mime_type = file.get('mimetype', 'fish/sticks')
        # Grabs the comment from the payload
        comment_text = comment.get('comment', '')

        # If the comment is empty or the first character isn't a /, move on.
        if not comment_text or not comment_text[0].startswith('/'):
            return

        # Splits the string on the spaces and slices the array to separate 
        # the command from the rest.
        split_comment = comment_text.split()
        # Replaces the /
        command = split_comment[:1][0].replace('/', '')
        modifiers = split_comment[1:]

        # Checks what kind of file this is (text, image, video, application)
        # so we can check the command against available command for that type.
        file_type = mime_type.split('/')[0]

        # Gets the user id to use later in an @message to notify success 
        # or to offer feedback/help in the case of an incorrect command
        user_id = comment.get('user')
        file_id = file.get('id')

        test_message = {
            "type": "message",
            "channel": "C051J2BPB",
            "text": 'File received a command: {}'.format(command)
        }
        self.sendMessage(json.dumps(test_message).encode('utf-8'))

        logger.info('File received a command: {}'.format(command))
        logger.info(payload)

    def onClose(self, wasClean, code, reason):
        logger.info("WebSocket connection closed: {0}".format(reason))
