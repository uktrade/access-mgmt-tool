# -*- coding: utf-8 -*-
from github.web_requests import WebRequests


def test_raise_error_if_used_getter_before_assigning_client_an_instance(
    gh_queries, caplog
):
    try:
        gh_queries.gh_client
        assert False
    except ValueError:
        assert "You must set the gh_client before using it" in caplog.messages
        assert True


def test_gh_client_returns_expected_instace_class(gh_queries, live_gh_client, caplog):
    gh_queries.gh_client = live_gh_client
    assert isinstance(gh_queries.gh_client, WebRequests)
