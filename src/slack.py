import requests
import logging
logger = logging.getLogger('app')


class SlackError(Exception):
    pass


def fetch_from_slack(method: str, token: str) -> dict:
    ''' This function makes a POST request to the slack API. 
        Pass in the Slack token to use for auth (create a bot, rather than use
        a personal token). If there is any trouble coming from the Slack server
        or if the token doesn't successfully allow authorization, raises a
        SlackError. Otherwise, returns the response body.
    '''

    # Set the method and the token on the url
    url = 'https://slack.com/api/{method}?token={token}'.format(
        method=method,
        token=token
    )

    try:
        # Make a call to the slack API
        resp = requests.post(url)
    except requests.exceptions.ConnectionError as err:
        # If there is a connection error on either end, raise an error
        error = 'ConnectionError connecting to {url}. {error}'.format(
            url=url,
            error=err
        )
        raise SlackError(error)
    else:
        # Parse the response 
        body = resp.json()

    # Check the status code for anything other than 200
    if resp.status_code != 200:
        error = 'Couldn\'t connect to Slack API. Status code: {code}'.format(
            code=resp.status_code
        )
        raise SlackError(error)

    # Slack includes an `ok` key to check 
    if not body.get('ok', False):
        error = 'Error authorizing with slack: {error}'.format(
            error=body.get('error')
        )
        raise SlackError(error)

    return body
