# -*- coding: utf-8 -*-
"""
This test needs to be manual and run in isolation as of now
- since we can not remove/delete user until user has accepted inviitation
- trying to remoe user will result in 404
so to execte this test
 - accept tthe invitation
 - un comment codes
 - pytest tests/github/gh_queries/unit/test_github_remove_member_from_an_organization.py
"""
# def test_github_remove_member_from_an_organization(
#     real_test, live_gh_queries, gh_query_urls,github_handle,
# ):

#     try:
#         members_url = gh_query_urls.organization_members_url
#         live_gh_queries.remove_user_from_an_organization(members_url=members_url,github_handle=github_handle)
#         assert True
#     except:
#         assert False
