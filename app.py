import configparser
from src.slack import get_rtm_url, SlackError
import logging

config = configparser.ConfigParser()

def run():
    config.read('/etc/slack.ini')
    slack_api_token = config['default']['slack_api_token']
    try:
        url = get_rtm_url(slack_api_token)
        logging.info('Got Slack webhook URL: {url}.'.format(url=url))
    except SlackError as error:
        logging.error(error)
        exit(1)

if __name__ == '__main__':
    run()
