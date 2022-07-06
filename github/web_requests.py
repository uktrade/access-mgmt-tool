# -*- coding: utf-8 -*-
import requests
import logging
from .functions import url_checker, isinstance_of, isempty_string


logger = logging.getLogger(__name__)


class WebRequests:
    """
    A simple wrapper to requests library which
     - authenticates against given api end point
     - POST the requested payload
    """

    def __init__(self, verify_ssl=True):
        """
        Initalize values to be used with class

        Parameters:
        -----------
        url : str. you must provide this parameter
        verify_ssl: boolean. defaults to true

        Variables: All variables here are private and used internally by class
        ----------
        self._session : variable to hold session context
        self._response : dict. this varialbe holds the response from api server
        self._url : str
        self._verify_ssl: boolean , default to True
        self._auth_header: sets auth header with token or bearer
        self._token: keeps token handy
        """
        isinstance_of(verify_ssl, bool, "verify_ssl")
        self._url = ""
        self._verify_ssl = verify_ssl
        self._session = requests.session()
        self._response = {}
        self._auth_header = {}
        self._token = ""

    def clear(self):
        """
        Method to  clear values  from all class variables
        """
        self._url = ""
        self._response = {}
        self._response = {}
        self._auth_header = {}
        self._token = ""

    def __del__(self):
        """
        Destroctor: Method called when object id destroyed
        it simply claer all variables
        """
        self.clear()

    def _is_valid_header(self, header):
        if not (header == self.token_auth_header or header == self.bearer_auth_header):
            message = "auth_header must be set to token or Bearer type"
            logger.info(message)
            raise ValueError("message")

    @property
    def url(self):
        isempty_string(self._url, "url")
        return self._url

    @url.setter
    def url(self, end_point):
        isempty_string(end_point, "url")
        url_checker(end_point)
        self._url = end_point

    @property
    def verify_ssl(self):
        return self._verify_ssl

    @verify_ssl.setter
    def verify_ssl(self, verify_ssl):
        isinstance_of(verify_ssl, bool, "verify_ssl")
        self._verify_ssl = verify_ssl

    @property
    def token_auth_header(self):
        return {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "token ",
            "Content-Type": "application/json; charset=utf-8",
        }

    @property
    def bearer_auth_header(self):
        return {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "Bearer ",
            "Content-Type": "application/json; charset=utf-8",
        }

    @property
    def auth_header(self):
        """
        returns auth header
        """
        isinstance_of(self._auth_header, dict, "auth_header")

        if not self._token:
            self._is_valid_header(header=self._auth_header)

        """ we need a way to mask token in logs here """
        return self._auth_header

    @auth_header.setter
    def auth_header(self, auth_header):
        isinstance_of(auth_header, dict, "auth_header")
        self._is_valid_header(header=auth_header)
        self._auth_header = auth_header

    @property
    def post_response(self):
        """Returns current reqest repose"""
        return self._response

    @property
    def delete_response(self):
        """Returns current reqest repose"""
        return self._response

    def auth_token(self, token):
        """
        This method sets token to header

        Paramters:
        ----------
        token: str. You must supply the github token here and it must not be empty
        """

        isinstance_of(token, str, "auth_token")

        isempty_string(token, "auth_token")

        self._token = token

        self._is_valid_header(header=self.auth_header)

        self.auth_header["Authorization"] += token

        logger.info("auth_token is set")

    auth_token = property(None, auth_token)

    @post_response.setter
    def post_query(self, payload):
        self.send_query(payload=payload, query_type="post")

    def delete_query(self):
        """Returns current reqest repose"""
        self.send_query(payload={}, query_type="delete")

    @property
    def get_response(self):
        return self._response

    def get_query(self, payload={}):
        self.send_query(payload=payload)

    def send_query(self, payload, query_type="get"):
        """
        This method sets response to request

        Parameter:
        -----------
        payload: str, it should be string object
        query_type: str , it defaults to get query , other possible value is post
        """

        isinstance_of(query_type, str, "query_type")

        if query_type not in ["get", "post", "delete"]:
            error_msg = f"query_type expected to be either get,post or delete but was {query_type}"
            logger.error(error_msg)
            raise TypeError(error_msg)

        """
        Ensure Auth Token is set before we post request
        """

        try:
            self._session.headers = self.auth_header

            if query_type == "post":
                isinstance_of(payload, str, "payload")
                self._response = self._session.post(
                    self.url, data=payload, verify=self.verify_ssl
                )

            elif query_type == "get":
                isinstance_of(payload, dict, "payload")
                self._response = self._session.get(
                    self.url, params=payload, verify=self.verify_ssl
                )

            elif query_type == "delete":

                self._response = self._session.delete(self.url, verify=self.verify_ssl)

            if self._response.status_code not in [200, 201, 204]:
                error_msg = (
                    f"Expected 200 but got {self._response.status_code} for {self.url}"
                )
                logger.info(error_msg)
                raise RuntimeError(error_msg)

            if self.post_response.text:
                content = self.post_response.json()

                if "errors" in content:
                    logger.info(f'Errors: {content["errors"]}')
                    raise Exception(content["errors"])

                if "error" in content:
                    logger.info(f'Error: {content["error"]}')
                    raise Exception(content["error"])

            logger.info(
                f"Success: {query_type.capitalize()} Query Response status: {self.post_response.status_code}"
            )

        except:
            if self.post_response:
                logger.info(
                    f"Failed: {query_type.capitalize()} Query Response status: {self.post_response.status_code}"
                )
                logger.debug(f"Error: {self.post_response.content}")

            raise
