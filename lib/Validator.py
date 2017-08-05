from lib.Constants import Constants
from lib.JsonValidator import JsonValidator

class Validator(Constants):

    _is_response = False

    def __init__(self):
        if self.__class__.__name__ == 'Response':
            self._is_response = True

    def validate_response_format(self, expected, response):
        JsonValidator(self._is_response).validate(expected, response)

    def validate_rule(self, expected, rules):
        JsonValidator(self._is_response).validate(expected, rules)