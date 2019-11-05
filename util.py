import base64
import codecs
import configparser
import hashlib
import hmac
from urllib.parse import quote_plus


def generate_hash(key_secret, query_string=None):
    """
    key_secret: The secret key associated with the API key you'll be passing in the `api_key` parameter. It is a tuple
        with the following format: (KEY_ID, KEY_SECRET)
    query_string: A URL query string

        query_string format: "param1=value1&param2=value2&api_key=API_KEY"

        Note that this does not have the leading "?" and that the api_key is included
    """
    hash = hmac.new(codecs.encode(key_secret[1]), codecs.encode(query_string), hashlib.sha256).digest()
    hash = base64.b64encode(hash)
    hash = quote_plus(hash)
    return hash


def generate_full_endpoint(api_url, endpoint, key_secret=None, query_string=None):
    """Build the full API end point with query string and auth hash

    api_url: The base URL for the API
    endpoint: The URL that will be queried
    key_secret: The key associated with the user making this call. It is a tuple
        with the following format: (KEY_ID, KEY_SECRET)
    query_string: The query string that will be used to make this call

    Returns the full URL of the API, with auth_hash, query string and api_key
    for this call
    """
    if query_string:
        query_string = "{query_string}&".format(query_string=query_string)
    else:
        query_string = ""
    if key_secret:
        query_string += "api_key={api_key}".format(api_key=key_secret[0])
        query_string += "&auth_hash={hash}".format(
            hash=generate_hash(key_secret, query_string))
    query_string = "?{query_string}".format(query_string=query_string)

    url = "{api}{endpoint}{query_string}".format(
        api=api_url,
        endpoint=endpoint,
        query_string=query_string)
    return url


def get_secrets():
    config = configparser.ConfigParser()
    config.read('secrets.ini')
    return config['DEFAULT']


def generate_url(endpoint, query_params=None):
    secrets = get_secrets()
    key_id = secrets['key_id']
    key_secret = secrets['key_secret']
    api_url = secrets['api_url']
    return generate_full_endpoint(api_url, endpoint, key_secret=(key_id, key_secret), query_string=query_params)
