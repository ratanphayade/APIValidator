import json
from urllib.parse import urlencode
from lib.Validator import Validator
class Header(Validator):

    payload = None

    headers = {}

    __header_options = {}


    def __init__(self):
        self.header_options = self.rules['request']['headers']


    def has_payload(self):
        if 'content_type' not in self.__header_options:
            return False
        elif 'payload' not in self.__header_options:
            return False
        return True


    def format_payload(self):
        if not self.has_payload():
            return
        elif self.__header_options['content_type'] == 'json':
            self.payload = json.loads(json.dumps(self.__header_options['payload']))
        else:
            self.payload = urlencode(self.__header_options['payload'])
        self.set_content_type()


    def set_content_type(self):
        self.headers['content_type'] = self.CONTENT_TYPES[self.__heafer_options['content_type']]        


    def has_headers(self):
        if self.__header_options is None:
            return False
        return True
        

    def format_request_headers(self):
        if not self.has_headers():
            return
        self.format_payload()
        self.append_custom_headers()

    def append_custom_headers(self):
        if 'custom_header' not in self.__header_options:
            return
        self.add_custom_headers(
            self.execute_method(self.__header_options['custom_header'])
        )

    def execute_method(self, method_name):
        method = None
        try:
            method = getattr(self, method_name)
        except AttributeError:
            raise NotImplementedError("Class `{}` does not implement `{}`".format(self.__class__.__name__, method_name))
        method()

    def add_custom_headers(self, custom_headers):
        if type(custom_headers) is not dict:
            print('header should be dict type')
            exit()
        self.headers.update(custom_headers)
            