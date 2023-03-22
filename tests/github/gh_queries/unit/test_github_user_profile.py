# -*- coding: utf-8 -*-
from django.conf import settings


def test_github_user_profile_for_non_exising_user(
    real_test, live_gh_queries, gh_query_urls, caplog
):
    github_handle = "thisIsVeryRandomUserNameIbetNoOneThoughtOfThisBefore872020976252"

    profile = live_gh_queries.user_profile(
        url=gh_query_urls.users_root_url, github_handle=github_handle
    )

    assert f"{github_handle} profile not found" in caplog.messages
    assert profile == {}


def test_github_user_profile_for_an_exising_user(
    real_test, live_gh_queries, gh_query_urls
):
    github_handle = settings.TEST_GIT_ACCOUNT
    profile = live_gh_queries.user_profile(
        url=gh_query_urls.users_root_url, github_handle=github_handle
    )
    assert profile
