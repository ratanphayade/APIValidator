from lib.Constants import Constants
from lib.JsonValidator import JsonValidator

class Validator(Constants):
    """
    This class manages all aspects of validation
    It will identify the type of data before validating 
    and based on the type validation takes place
    """

    _is_response = False
    """
    bool: flag which indicated whether the object is belongs to response 
    """

    def __init__(self):
        """
        Initializes the object 
        set the flag to identify whether the class belongs to response
        """
        if self.__class__.__name__ == 'Response':
            self._is_response = True

    def validate_response_format(self, expected, response):
        """
        Validates the response against the expected format

        Args:
            expected (dict): expected response format
            response (dict): response of the endpoint
        """
        JsonValidator(self._is_response).validate(expected, response)

    def validate_rule(self, expected, rules):
        """
        Validates the rules provided 
        Rules should have minimum required info

        Args:
            expected (dict): expected rule format
            rules (dict): provided rule
        """
        JsonValidator(self._is_response).validate(expected, rules)

    def get_attribute(self, data_set, key, default_return_value, data_type = None):
        """
        fetches the attribute specified by the `key` from the data set specified by `data_set`
        in case of not found or empty data default value is returned which is specified by `default_return_value`
        if `data_type` is specified then data type check will be done

        Args:
            data_set (dict): data set from which attribute should be fetched
            key (str): attribute to be fetched from the data set
            default_return_value (any): default return value if `key` is not present or evaluated to false
            data_type (type, optional): data type to which the result should belong
        """
        if key not in data_set:
            return default_return_value
        elif not bool(data_set[key]):
            return default_return_value
        elif data_type and type(data_set[key]) != data_type:
            print('Data type missmatch for the data key ' + str(key) + '. It should be of type ' + data_type)
            exit()
        else:
            return data_set[key]
            