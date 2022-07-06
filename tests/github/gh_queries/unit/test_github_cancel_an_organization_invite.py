# -*- coding: utf-8 -*-
def test_github_cancel_invitation(
    real_test, live_gh_queries, gh_query_urls, github_handle, gh_user_id, gh_team_ids
):
    invitation_url = gh_query_urls.organization_invitations_url

    if live_gh_queries.invite_user_to_an_organization(
        invitation_url=invitation_url, user_id=gh_user_id, team_ids=gh_team_ids
    ):
        # ensure user is invited before cancelling invite
        live_gh_queries.pending_invites = invitation_url

        assert github_handle in live_gh_queries.pending_invites

        invitation_id = live_gh_queries.pending_invites[github_handle]
        live_gh_queries.cancel_invitation(
            invitation_url=invitation_url, invitation_id=invitation_id
        )

        # Now Invite should not be found
        live_gh_queries.pending_invites = invitation_url
        assert github_handle not in live_gh_queries.pending_invites

    else:
        assert False
