# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode
from lib.Validator import Validator
class Header(Validator):
    """
    This class is responsible for request and response header management
    It sets the header and also takes care of the payload in case of request
    This will manage the custom header to be set for the request
    This will help to identify the required headers and validate the response

    Attributes:
        payload (dict): Holds the payloads required for the current request
        headers (dict): Holds all the header information for the current request or response
        __header_options (dict): Its the collection of all the header
            configuration for the current request or response

    """
    payload = None
    """
    dict: payload of the request

    Holds the request payload.
    It will be converted to the required format based on the request type.
    """

    headers = {}
    """
    dict: header information of request or response

    Holds all the header details for request and response (based on type)
    It can also be empty
    """

    __header_options = {}
    """
    dict: header option of the request or response

    These header options will be taken from the rule file
    for both request and response based on its type.
    This will be used in all the places to identify the required field
    """

    def __init__(self, rule):
        """
        Initializes the header option data for the request and response

        This will initialize the header option based on which object its initiated from
        for request the rule will be have data related to request,
        for response the rule will be have data related to response

        Args:
            rule: request rule configuration for requesr ot response based

        """
        self.__header_options = self.get_attribute(
            rule
            , 'headers'
            , {}
        )

    def format_payload(self):
        """
        gets the payload form the request headers as specified
        it currently supports 2 types of content type json | x-www-form-urlencoded
        the payload is formated based on the content type
        if no content type is given then default json will be considered
        """
        payload = self.get_attribute(
            self.__header_options
            , 'payload'
            , {}
        )
        if self.set_content_type() == 'json':
            self.payload = json.loads(json.dumps(payload))
        else:
            self.payload = urlencode(payload)


    def set_content_type(self):
        """
        Sets the content type of the request or response
        in case content type is not defined then will consider the default content type (json)
        """
        content_type = self.get_attribute(
            self.__header_options
            , 'content_type'
            , self.DEFAULT_CONTENT_TYPE
        )
        self.headers['content_type'] = self.CONTENT_TYPES[content_type]
        return content_type


    def has_headers(self):
        """
        Checks whether the request or response has the header option specified in the rules
        """
        if self.__header_options is None:
            return False
        return True

    def format_request_headers(self):
        """
        Formates the request headers
        formates the payload of the reuqest based on the content type specified
        in case the content type is not specified it'll consider default as json
        It also appends the custom headers specified by in the rule
        """
        if not self.has_headers():
            return
        self.format_payload()
        self.append_custom_headers()

    def append_custom_headers(self):
        """
        Adds additional header details specified in the rule file
        additional headers will be added only if custom_header is defined in the rules
        custom_header will be a string which will idicate the method name
        which will calculate the custom header and return in dict form
        """
        custom_header_generator = self.get_attribute(
            self.__header_options
            , 'custom_header'
            , None
        )
        if custom_header_generator is not None:
            self.add_custom_headers(
                self.execute_method(custom_header_generator)
            )

    def execute_method(self, method_name):
        """
        Checks for the existance of method specidied in custom_header
        if exist calls the method and returns the data

        Args:
            method_name (str): custom method to be executed

        Returns:
            dict: additional header data to be append with request

        Raises:
            NotImplementedError: when the custom method defination is not found or out of scope
        """
        method = None
        try:
            method = getattr(self, method_name)
        except AttributeError:
            raise NotImplementedError(
                "Class `{}` does not implement `{}`".format(self.__class__.__name__, method_name)
            )
        return method()

    def add_custom_headers(self, custom_headers):
        """
        Appends the custom header data to the header
        Checks the data type of custom_headers before updateing the header
        data type should be dict in order to contunue with validation
        """
        if type(custom_headers) is not dict:
            print('header should be dictionary type')
            exit()
        self.headers.update(custom_headers)
            