# -*- coding: utf-8 -*-
def test_github_invited_members_list(
    real_test, live_gh_queries, gh_query_urls, github_handle, gh_user_id, gh_team_ids
):
    invitation_url = gh_query_urls.organization_invitations_url

    if live_gh_queries.invite_user_to_an_organization(
        invitation_url=invitation_url, user_id=gh_user_id, team_ids=gh_team_ids
    ):
        live_gh_queries.pending_invites = invitation_url

        assert github_handle in live_gh_queries.pending_invites

    else:
        assert False
