import requests
import logging
logger = logging.getLogger('app')


class SlackError(Exception):
    pass


def get_rtm_url(token: str) -> str:
    ''' This function makes a POST request to the slack API's rtm.start method.
        Pass in the slack token to use for auth (create a bot, rather than use
        a personal token). If there is any trouble coming from the Slack server
        or if the token doesn't successfully allow authorization, raises a
        SlackError. Otherwise, returns the url.
    '''

    rtm_start_url = 'https://slack.com/api/rtm.start?token={token}'.format(
        token=token
    )

    try:
        resp = requests.post(rtm_start_url)
    except requests.exceptions.ConnectionError as err:
        error = 'ConnectionError connecting to {url}. {error}'.format(
            url=rtm_start_url,
            error=err
        )
        raise SlackError(error)
    else:
        body = resp.json()
        url = body.get('url')

    if resp.status_code != 200:
        error = 'Couldn\'t connect to Slack API. Status code: {code}'.format(
            code=resp.status_code
        )
        raise SlackError(error)

    if not body.get('ok', False):
        error = 'Error authorizing with slack: {error}'.format(
            error=body.get('error')
        )
        raise SlackError(error)

    return url
