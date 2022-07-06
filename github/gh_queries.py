# -*- coding: utf-8 -*-
from django.conf import settings
import logging
import json

logger = logging.getLogger(__name__)


class GHQueries:
    """
    This class make use of the web reuqest to send get/post request for fetching required data
    """

    def __init__(
        self,
    ):
        self._gh_client = None
        self._members = []
        self._teams = {}
        self._invited_members = {}

    def clear_data(self):
        self._members = []
        self._teams = {}
        self._invited_members = {}

    def clear(self):
        self.clear_data()
        self._gh_client = None

    def __del__(self):
        self.clear()

        if self._gh_client:
            self.gh_client.clear()

    def _get_data(self, url):
        """
        it loops through the get request until it fetches all data and, returns list of raw data

        Paramters:
        ----------
        - url: this is end point for get request

        Returns:
        --------
        list of raw data, fetched from api endpoint
        """
        self.gh_client.url = url
        payload = {"role": "all", "per_page": 100, "page": 1}

        data = []
        while True:
            self.gh_client.get_query(payload=payload)
            response = self.gh_client.get_response.json()

            if response:
                data += response
                payload["page"] = payload["page"] + 1
            else:
                break

        return data

    def _get_single_data(self, url):
        """
        it gets the data from end point which returns dict for single entiry
        such as github user, org memember (not members!)
        Paramters:
        ----------
        - url: this is end point for get request

        Returns:
        --------
        dict of raw data, fetched from api endpoint
        """
        self.gh_client.url = url

        self.gh_client.get_query(payload={})
        response = self.gh_client.get_response.json()

        return response

    @property
    def gh_client(self):
        """
        return instance of the github api client if set , or rasise RuntimError

        Paramters:
        ---------
        None

        Depends On
        ----------
        None

        Returns:
        --------
         - Error or an instance of github api client
        """
        if not self._gh_client:
            error_msg = "You must set the gh_client before using it"
            logger.info(error_msg)
            raise ValueError(error_msg)

        return self._gh_client

    @gh_client.setter
    def gh_client(self, client):
        """
        sets the github api client to supplied object instance

        Paramters:
        ----------
        None

        Depends on:
        -----------
        None

        Retruns:
        --------
        Nothing
        """
        self._gh_client = client

    @property
    def organization_members(self):
        if not self._members:
            logger.info("Empty memberlist, may be you should set the url first?")
        return self._members

    @organization_members.setter
    def organization_members(self, url):
        """
        Get github handle for all org members

        Parameters:
        ----------
        None

        Depends on:
        -----------
        None

        Returns:
        --------
        List of all org members
        """
        for data in self._get_data(url=url):
            self._members.append(data["login"])

        return self._members

    def user_is_an_organization_member(self, members_url, github_handle):
        """
        Check if user is already member of a given github organisation
        Github returns reponsecode 204 if user is member of org and 404 otherwise

        Parameters:
        -----------
        - members_url, string url to root of members
        - github_handle, id that we need to check against
        Depends on:
        -----------
        None

        Returns:
        --------
         Boolean True is user is member of org , False if not
        """

        try:
            url = "/".join([members_url, github_handle])
            self.gh_client.url = url
            self.gh_client.get_query()

            if self.gh_client.get_response.status_code == 204:
                return True
            return False
        except:
            return False

    @property
    def organization_teams(self):
        if not self._teams:
            logger.info("Empty teams, may be you should set the url first?")

        return self._teams

    @organization_teams.setter
    def organization_teams(self, url):
        """
        Get all the teams for given organization
        and assign them to self._teams dict

        Paramters:
        ----------
        None

        Returns:
        --------
        None
        """
        for team in self._get_data(url=url):
            self._teams.update({team["name"]: team["id"]})

    def team_id(self, team_name):
        """
        find team id of a given team

        Parameter:
        ---------
         - team_name: name of the team , str object

        Depends on
        ----------
        - organization_teams

        Returns:
        --------
         - team id, if found if not it returns 0 and, loggs info message
        """
        if self.organization_teams:
            if team_name in self.organization_teams:
                return self.organization_teams[team_name]
            else:
                logger.info(f"{team_name} not found in {settings.GITHUB_ORG_NAME}")
                return 0

    def user_profile(self, url, github_handle):
        """
        Get github user profile information, key thing we are interested in are
        - id , which is useful for creating actual invite
        - name, which can be used to determine if user have full name in profile or not
         this can be manual check box which can be validated at the time of createing access request

         Limitation, it can only fetch and store one user profile at a time

        Paramters:
        ----------
        - url: takes a root url to access github  users which is https://api.github.com/users
        - github_handle: github user name used to from the url

        Depends on
        ----------
        None

        Returns:
        --------
        - empty user dict ( if user does not exists on github) or dictory with public user profile which contains id and login

        Note:
        -----
        - it additionally logges info about user not being found on github
        - user profile id is what we can use for preparing actual invite
        """

        try:
            profile_url = "/".join([url, github_handle])
            user_profile = self._get_single_data(url=profile_url)
        except:
            user_profile = {}

            error_msg = f"{github_handle} profile not found"
            logger.info(error_msg)

        return user_profile

    @property
    def pending_invites(self):
        return self._invited_members

    @pending_invites.setter
    def pending_invites(self, invitation_url):
        self._invited_members.clear()
        for member in self._get_data(url=invitation_url):
            self._invited_members.update({member["login"]: member["id"]})

    def cancel_invitation(self, invitation_url, invitation_id):
        try:
            cancle_invite_url = "/".join([invitation_url, str(invitation_id)])
            self.gh_client.url = cancle_invite_url
            self.gh_client.delete_query()
        except:
            logger.info("Failed: can not cancle invite")
            raise

    def invite_user_to_an_organization(self, invitation_url, user_id, team_ids=[]):
        """
        send out the inviattion for user to join the organization

        Paramters:
        ----------
        - invitation_url: github organization invitation end point
        - user_id: string to hold github handle
        - team_ids: list of team ids
        Depends on
        ----------
        - organization_teams
        - user profile
        - team_id
        """

        try:

            invitation_data = {
                "invitee_id": user_id,
                "role": "direct_member",
                "team_ids": team_ids,
            }

            self.gh_client.url = invitation_url
            self.gh_client.post_query = json.dumps(invitation_data)
            return True
        except:
            raise

    def remove_user_from_an_organization(self, members_url, github_handle):

        try:
            url = "/".join([members_url, github_handle])
            self.gh_client.url = url
            self.gh_client.delete_query()
        except:
            logger.info("Failed: can not remove member from an org")
            raise
