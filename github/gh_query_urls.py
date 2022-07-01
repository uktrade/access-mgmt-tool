# -*- coding: utf-8 -*-
from github.web_requests import WebRequests
from django.conf import settings
from github.functions import isinstance_of


class GHQueryUrls:
    """
    This class simply returns the url end points
    """

    def __init__(self):
        pass

    def clear(self):
        pass

    @property
    def organization_url(self):
        return "/".join(
            [settings.GITHUB_API_URL.rstrip("/"), "orgs", settings.GITHUB_ORG_NAME]
        )

    @property
    def organization_members_url(self):
        return "/".join([self.organization_url, "members"])

    @property
    def organization_teams_url(self):
        return "/".join([self.organization_url, "teams"])

    @property
    def organization_invitations_url(self):
        return "/".join([self.organization_url, "invitations"])

    @property
    def users_root_url(self):
        return "/".join([settings.GITHUB_API_URL.rstrip("/"), "users"])
