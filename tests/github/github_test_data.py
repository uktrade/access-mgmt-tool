# -*- coding: utf-8 -*-
from github.web_requests import WebRequests
from github.gh_query_urls import GHQueryUrls
from github.gh_queries import GHQueries

from django.conf import settings


class GithubRealTestData:
    def __init__(self, github_handle, teams):
        self._gh_client = WebRequests(verify_ssl=True)
        self._gh_client.auth_header = self._gh_client.token_auth_header
        self._gh_client.auth_token = settings.GITHUB_AUTH_TOKEN

        self._gh_query_urls = GHQueryUrls()
        self._gh_queries = GHQueries()

        self._gh_queries.gh_client = self._gh_client

        self._github_handle = github_handle

        self._profile = {}
        self._team_ids = []
        self._teams = teams

    def user_profile(self):
        self._profile = self._gh_queries.user_profile(
            url=self._gh_query_urls.users_root_url, github_handle=self._github_handle
        )

    def set_team_ids(self):
        self._gh_queries.organization_teams = self._gh_query_urls.organization_teams_url

        for team in self._teams:
            id = self._gh_queries.team_id(team_name=team)
            if id:
                self._team_ids.append(id)

    @property
    def github_handle(self):
        return self._github_handle

    @property
    def user_id(self):
        return self._profile["id"]

    @property
    def teams(self):
        return self._teams

    @property
    def team_ids(self):
        return self._team_ids


gh_test_data = GithubRealTestData(
    github_handle=settings.TEST_GIT_ACCOUNT, teams=settings.TEST_GIT_TEAMS
)
gh_test_data.user_profile()
gh_test_data.set_team_ids()


def test_user_id():
    global gh_test_data
    return gh_test_data.user_id


def test_github_handle():
    global gh_test_data
    return gh_test_data.github_handle


def test_team_ids():
    global gh_test_data
    return gh_test_data.team_ids
