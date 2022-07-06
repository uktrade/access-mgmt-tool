# -*- coding: utf-8 -*-
def test_non_existing_github_user_is_an_organization_member(
    real_test, live_gh_queries, gh_query_urls
):
    member_exist = live_gh_queries.user_is_an_organization_member(
        members_url=gh_query_urls.organization_members_url,
        github_handle="this-does-not-exist",
    )
    assert member_exist == False


def test_existing_github_user_is_an_organization_member(
    real_test, live_gh_queries, gh_query_urls
):
    """
    We are getting list of all the members and test the first one
    it must return true unless something wrong with our queries
    """
    live_gh_queries.organization_members = gh_query_urls.organization_members_url
    member_exist = live_gh_queries.user_is_an_organization_member(
        members_url=gh_query_urls.organization_members_url,
        github_handle=live_gh_queries.organization_members[0],
    )
    assert member_exist == True
