# -*- coding: utf-8 -*-
def test_github_organization_teams(real_test, live_gh_queries, gh_query_urls):
    """
    It is difficult to test against name of actual members
    as people joining/leaving is very dymanic and count of members
    will always vary , however it is safe to assume there is least one member
    """
    live_gh_queries.organization_teams = gh_query_urls.organization_teams_url
    assert len(live_gh_queries.organization_teams) > 1


def test_empty_github_organization_team_logs_info(real_test, live_gh_queries, caplog):
    live_gh_queries.clear_data()
    live_gh_queries.organization_teams
    assert "Empty teams, may be you should set the url first?" in caplog.messages
