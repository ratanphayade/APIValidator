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

    def get_attribute(self, data_set, key, default_return_value, data_type):
        if key not in data_set:
            return default_return_value
        elif not bool(data_set[key]):
            return default_return_value
        elif data_type and type(data_set[key]) != data_type:
            print('Data type missmatch for the data key ' + str(key) + '. It should be of type ' + data_type)
            exit()
        else:
            return data_type[key]
            