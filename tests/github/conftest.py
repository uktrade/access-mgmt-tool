# -*- coding: utf-8 -*-
import pytest
from django.conf import settings
from github.web_requests import WebRequests
from github.gh_query_urls import GHQueryUrls
from github.gh_queries import GHQueries
from .github_test_data import test_user_id, test_team_ids, test_github_handle


@pytest.fixture(scope="session")
def web_request():
    web_request = WebRequests(verify_ssl=True)
    yield web_request
    web_request.clear()


@pytest.fixture(scope="module")
def dummy_gh_query_urls():
    api_url = settings.GITHUB_API_URL
    org_name = settings.GITHUB_ORG_NAME

    settings.GITHUB_API_URL = "https://dummy.url"
    settings.GITHUB_ORG_NAME = "acme"

    dummy_gh_query_urls = GHQueryUrls()
    yield dummy_gh_query_urls

    dummy_gh_query_urls.clear()

    settings.GITHUB_ORG_NAME = org_name
    settings.GITHUB_API_URL = api_url


@pytest.fixture(scope="session")
def gh_query_urls():
    gh_query_urls = GHQueryUrls()
    yield gh_query_urls
    gh_query_urls.clear()


@pytest.fixture(scope="session")
def live_gh_client():
    live_gh_client = WebRequests(verify_ssl=True)
    live_gh_client.auth_header = live_gh_client.token_auth_header
    live_gh_client.auth_token = settings.GITHUB_AUTH_TOKEN

    yield live_gh_client

    live_gh_client.clear()


@pytest.fixture(scope="module")
def live_gh_queries(live_gh_client):
    live_gh_queries = GHQueries()
    live_gh_queries.gh_client = live_gh_client
    yield live_gh_queries
    live_gh_queries.clear()


@pytest.fixture(scope="function")
def gh_queries():
    gh_queries = GHQueries()
    yield gh_queries
    gh_queries.clear()


@pytest.fixture(scope="session")
def real_test():
    if not (settings.DEPLOYMENT_ENVIRONMENT == "real_test"):
        pytest.skip(
            reason="These tests are against real endpoints, they needs a valid credentials. if you want to run the, set DEPLOYMENT_ENVIRONMENT to 'real_test' in evironment"
        )


def pytest_generate_tests(metafunc):
    """
    overrride pytest function to generate tests with parameters

    Parameters
    -----------
    metafunc: function to be parameterized, in this case all tests
    """

    global invitation_data

    parameters = ["gh_user_id", "gh_team_ids"]

    if set(parameters).issubset(set(metafunc.fixturenames)):

        if "github_handle" in set(metafunc.fixturenames):
            parameters.append("github_handle")
            metafunc.parametrize(
                parameters, [[test_user_id(), test_team_ids(), test_github_handle()]]
            )

        else:
            metafunc.parametrize(parameters, [[test_user_id(), test_team_ids()]])

    elif "github_handle" in set(metafunc.fixturenames):
        metafunc.parametrize(["github_handle"], [[test_github_handle()]])
