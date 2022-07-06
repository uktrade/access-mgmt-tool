# -*- coding: utf-8 -*-
def test_github_organization_url(dummy_gh_query_urls):
    assert dummy_gh_query_urls.organization_url == "https://dummy.url/orgs/acme"


def test_github_organization_members_url(dummy_gh_query_urls):
    assert (
        dummy_gh_query_urls.organization_members_url
        == "https://dummy.url/orgs/acme/members"
    )


def test_github_organization_teams_url(dummy_gh_query_urls):
    assert (
        dummy_gh_query_urls.organization_teams_url
        == "https://dummy.url/orgs/acme/teams"
    )


def test_github_organization_invitations_url(dummy_gh_query_urls):
    assert (
        dummy_gh_query_urls.organization_invitations_url
        == "https://dummy.url/orgs/acme/invitations"
    )


def test_github_users_root_url(dummy_gh_query_urls):
    assert dummy_gh_query_urls.users_root_url == "https://dummy.url/users"
