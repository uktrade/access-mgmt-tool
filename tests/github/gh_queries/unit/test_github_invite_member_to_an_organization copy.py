# -*- coding: utf-8 -*-
def test_github_invite_member_to_an_organization(
    real_test, live_gh_queries, gh_query_urls, gh_user_id, gh_team_ids
):
    invitation_url = gh_query_urls.organization_invitations_url
    result = live_gh_queries.invite_user_to_an_organization(
        invitation_url=invitation_url, user_id=gh_user_id, team_ids=gh_team_ids
    )
    assert result == True
