# -*- coding: utf-8 -*-
def test_get_query_response(web_request, caplog):
    try:
        web_request.auth_header = web_request.token_auth_header
        web_request.auth_token = "some token"
        web_request.url = "https://httpbin.org/get"
        web_request.get_query()
        web_request.clear()
        assert f"Success: Get Query Response status: 200" in caplog.messages
        assert True
    except:
        assert False


def test_get_query_failed_response(web_request, caplog):
    url = "https://httpbin.org/post"
    try:
        web_request.auth_header = web_request.token_auth_header
        web_request.auth_token = "some token"
        web_request.url = url
        web_request.get_query()
        assert False
    except RuntimeError:
        web_request.clear()
        assert f"Expected 200 but got 405 for {url}" in caplog.messages
        assert True
