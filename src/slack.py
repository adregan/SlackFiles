import requests
import logging
logger = logging.getLogger('app')


class SlackError(Exception): pass

def get_rtm_url(token):
    rtm_start_url = 'https://slack.com/api/rtm.start?token={token}'.format(
        token=token
    )

    logger.info('Connecting to https://slack.com/api/rtm.start')

    resp = requests.post(rtm_start_url)

    if resp.status_code != 200:
        err = 'Couldn\'t connect to Slack API. Status code: {code}'.format(
            code=resp.status_code
        )
        raise SlackError(err)

    body = resp.json()

    if not body.get('ok', False):
        err = 'Error authorizing with slack: {error}'.format(
            error=body.get('error')
        )
        raise SlackError(err)

    url = body.get('url')

    return url
