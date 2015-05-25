import logging
import asyncio
import json
from autobahn.asyncio.websocket import WebSocketClientProtocol
from .slack import fetch_from_slack, SlackError

logger = logging.getLogger('app')


class SlackClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        logger.info("Server connected: {0}".format(response.peer))

    @asyncio.coroutine
    def onOpen(self):
        logger.info("WebSocket connection open.")

        while True:
            try:
                resp = yield from fetch_from_slack('im.list')
            except SlackError as error:
                logger.error(error)
            else:
                self.dm_user = {
                    im.get('user'): im.get('id')
                    for im in resp.get('ims')
                }
                logger.info('Updated direct message user data')

            # Repeat this every 30 minutes
            yield from asyncio.sleep(1800)

    def onMessage(self, payload, isBinary):
        # The payload comes as bytes, decode before loading the JSON
        payload = json.loads(payload.decode('utf8'))

        # Only interested in the file comments
        if payload.get('type') != 'file_comment_added':
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
            "channel": self.dm_user.get(user_id),
            "text": 'File received a command: {}'.format(command)
        }
        self.sendMessage(json.dumps(test_message).encode('utf-8'))

        logger.info('File received a command: {}'.format(command))
        logger.info(payload)

    def onClose(self, wasClean, code, reason):
        logger.info("WebSocket connection closed: {0}".format(reason))
