from handler import is_valid_url, lambda_handler


def event(method, path, body=None):
    return {
        'requestContext': {'http': {'method': method}, 'domainName': 'x.test'},
        'rawPath': path,
        'body': body,
    }


def test_valid_urls():
    assert is_valid_url('https://example.com/a')
    assert not is_valid_url('javascript:alert(1)')
    assert not is_valid_url('not a url')


def test_bad_post_is_400():
    res = lambda_handler(event('POST', '/', '{"url": "nope"}'), None)
    assert res['statusCode'] == 400


def test_unknown_path_is_404():
    assert lambda_handler(event('GET', '/', None), None)['statusCode'] == 404
