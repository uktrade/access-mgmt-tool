# -*- coding: utf-8 -*-
from django.conf import settings


def test_team_id_when_teams_are_empty(real_test, live_gh_queries, caplog):
    live_gh_queries.clear_data()
    live_gh_queries.team_id(team_name="it-is-all-empty")
    assert "Empty teams, may be you should set the url first?" in caplog.messages


def test_team_id_when_team_does_not_exist(
    real_test, live_gh_queries, gh_query_urls, caplog
):
    team_name = "it-does-not-exist"
    live_gh_queries.organization_teams = gh_query_urls.organization_teams_url
    team_id = live_gh_queries.team_id(team_name=team_name)

    assert team_id == 0
    assert f"{team_name} not found in {settings.GITHUB_ORG_NAME}" in caplog.messages


def test_team_id_of_known_team(real_test, live_gh_queries, gh_query_urls):
    team_name = "read-only"
    expected_team_id = 5448562

    live_gh_queries.organization_teams = gh_query_urls.organization_teams_url
    team_id = live_gh_queries.team_id(team_name=team_name)

    assert expected_team_id == team_id
