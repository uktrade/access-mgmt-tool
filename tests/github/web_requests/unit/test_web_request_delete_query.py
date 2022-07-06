# -*- coding: utf-8 -*-


def test_github_delete_query(web_request, caplog):
    web_request.auth_header = web_request.token_auth_header
    web_request.auth_token = "some token"
    web_request.url = "https://httpbin.org/delete"
    web_request.delete_query()

    assert web_request.delete_response.status_code == 200
    assert f"Success: Delete Query Response status: 200" in caplog.messages

    web_request.clear()
