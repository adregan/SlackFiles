import urllib
from collections import namedtuple

Connection = namedtuple('Connection', ('host', 'port', 'ssl'))


def parse_url(url: str) -> namedtuple:
    ''' Parses a url and returns a namedtuple with the kind of values that
        asyncio's loop wants to make a connection. Inspired by 
        https://github.com/aaugustin/websockets/blob/master/websockets/uri.py
    '''
    # Parse the url using url lib
    parsed = urllib.parse.urlparse(url)

    # Grab the host, set ssl to a boolean (wss is a secure websocket)
    host = parsed.netloc
    ssl = parsed.scheme == 'wss'

    # If there is a port, use that. Otherwise 443 for secure, 80 for regular.
    if parsed.port:
        port = parsed.port
    elif ssl:
        port = 443
    else:
        port = 80

    return Connection(host, port, ssl)
