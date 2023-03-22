# -*- coding: utf-8 -*-
import logging
import re

logger = logging.getLogger(__name__)


def url_checker(url):
    """this regex can be improved a lot!"""
    url_regex = re.compile(r"^(https://|http://)")

    isinstance_of(variable=url, expected_type=str, variable_name="url")

    if not url_regex.match(url):
        message = f"Invalid url: {url}"
        logger.info(message)
        raise ValueError(message)


def isinstance_of(variable, expected_type, variable_name):

    """
    Reason why we are inplementing instance_of is, built-in isinstance would identify
    both date and,datetime as identical and, it does not provide way to
    enforce direct mapping

    Document: https://docs.python.org/3/library/functions.html#isinstance
    """
    if variable.__class__.__name__ != expected_type.__name__:
        error_msg = f"{variable_name} expected to be {expected_type.__name__} type but is {type(variable).__name__}"
        logger.info(error_msg)
        raise TypeError(error_msg)

    return True


def isempty_string(variable, variable_name):
    """
    ensure whay we have got is a of type string
    """
    isinstance_of(variable, str, variable_name)

    if not variable:
        message = f"{variable_name} must be set"
        logger.info(message)
        raise ValueError(message)

    return True
