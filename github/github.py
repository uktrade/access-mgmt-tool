# -*- coding: utf-8 -*-
from application.integration import AbstractIntegration

from github.web_requests import WebRequests
from github.gh_query_urls import GHQueryUrls
from github.gh_queries import GHQueries
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Github(AbstractIntegration):
    def __init__(self):

        gh_client = WebRequests()
        gh_client.url = settings.GITHUB_API_URL
        gh_client.auth_header = gh_client.token_auth_header
        gh_client.auth_token = settings.GITHUB_AUTH_TOKEN

        self._gh_quey_urls = GHQueryUrls()

        self._gh_queries = GHQueries()
        self._gh_queries.gh_client = gh_client

    def _refresh_data(self):
        self._gh_queries.organization_members = (
            self._gh_quey_urls.organization_members_url
        )
        self._gh_queries.organization_teams = self._gh_quey_urls.organization_teams_url

    def _add_member(self, github_handle, teams=[]):

        self._refresh_data()

        members_url = self._gh_quey_urls.organization_members_url
        team_ids = []

        if self._gh_queries.user_is_an_organization_member(
            members_url=members_url, github_handle=github_handle
        ):
            message = f"{github_handle} is already {settings.GITHUB_ORG_NAME} organization member"
            logger.info(message)

        else:
            """
            Get Team ids
            """
            for team in teams:
                team_ids.append(self._gh_queries.team_id(team_name=team))

            """
            send invite to user
            """
            invited_user = self._gh_queries.user_profile(
                url=self._gh_quey_urls.users_root_url, github_handle=github_handle
            )
            self._gh_queries.invite_user_to_an_organization(
                invitation_url=self._gh_quey_urls.organization_invitations_url,
                user_id=invited_user["id"],
                team_ids=team_ids,
            )

    def _remove_member(self, github_handle):
        """
        This method
         - Removes user (github_handle), if user is already a member of an organization
         - Cancle invitation if it is still pending to be accepted
        """

        self._refresh_data()
        members_url = self._gh_quey_urls.organization_members_url

        self._gh_queries.pending_invites = (
            self._gh_quey_urls.organization_invitations_url
        )

        if self._gh_queries.user_is_an_organization_member(
            members_url=members_url, github_handle=github_handle
        ):
            self._gh_queries.remove_user_from_an_organization(
                members_url=members_url, github_handle=github_handle
            )

        if github_handle in self._gh_queries.pending_invites:
            self._gh_queries.cancel_invitation(
                invitation_url=self._gh_quey_urls.organization_invitations_url,
                invitation_id=self._gh_queries.pending_invites[github_handle],
            )

        else:
            message = f"{github_handle} is not {settings.GITHUB_ORG_NAME} organization member(invitation may still be pending!)"
            logger.info(message)

    def grant_access(self, user_id, permissions: list[str]):
        """
        When we add member to github permission would render the teams that user should be added to
        by default we add it to none
        """
        try:
            self._add_member(github_handle=user_id, teams=permissions)
        except:
            raise

    def remove_access(self, user_id, permission: str):
        """
        When we remove user from a github organization, permission does not matter
        user gets removed from every where
        """
        try:
            self._remove_member(github_handle=user_id)
        except:
            raise
