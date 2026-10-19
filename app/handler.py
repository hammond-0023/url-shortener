import json
import os
import re
import secrets
import string
from urllib.parse import urlparse

import boto3

ALPHABET = string.ascii_letters + string.digits
CODE_RE = re.compile(r'^[A-Za-z0-9]{7}$')


def table():
    return boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])


def reply(status, body='', headers=None):
    return {'statusCode': status, 'headers': headers or {}, 'body': body}


def is_valid_url(url):
    if not isinstance(url, str) or len(url) > 2048:
        return False
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https') and bool(parsed.netloc)


def lambda_handler(event, context):
    method = event['requestContext']['http']['method']
    path = event['rawPath']

    if method == 'POST' and path == '/':
        try:
            url = json.loads(event.get('body') or '{}').get('url')
        except (ValueError, AttributeError):
            url = None
        if not is_valid_url(url):
            return reply(400, 'Send JSON like {"url": "https://example.com"}')
        code = ''.join(secrets.choice(ALPHABET) for _ in range(7))
        table().put_item(Item={'code': code, 'url': url})
        short = 'https://' + event['requestContext']['domainName'] + '/' + code
        return reply(201, json.dumps({'short_url': short}), {'Content-Type': 'application/json'})

    if method == 'GET' and CODE_RE.match(path[1:]):
        item = table().get_item(Key={'code': path[1:]}).get('Item')
        if item:
            return reply(302, '', {'Location': item['url']})

    return reply(404, 'Nothing here')

