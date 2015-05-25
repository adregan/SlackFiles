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
