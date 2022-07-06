# -*- coding: utf-8 -*-
from github.github import Github
from django.conf import settings


def test_adding_and_removing(real_test, github_handle):
    try:
        gh_access_mgmt = Github()
        gh_access_mgmt.grant_access(
            user_id=github_handle, permissions=settings.TEST_GIT_TEAMS
        )
        gh_access_mgmt.remove_access(user_id=github_handle, permission="")
        assert True
    except:
        assert False
