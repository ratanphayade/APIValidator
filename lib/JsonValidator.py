import re
import json

class JsonValidator():
    """
    This class manages all aspects of json data validation
    
    It will check for the valid formats based on the templates of response
    """
    
    _is_response = False
    """
    bool: flag which indicated whether the object is belongs to response 
    """

    def __init__(self, is_response):
        """
        Initialize the class
        initializes the reponse flag
        """
        self._is_response = is_response

    def validate(self, mandatory_fields, available_fields):
        """
        Validation starts here 
        this will check the type of data, based on which the data validation takes place

        Args:
            mandatory_fields (dict, list): madatory field list according to rule
            available_fields (dict, list): the data to validate for format
        """
        if type(mandatory_fields) is list:
            self.check_for_valid_format(mandatory_fields[0], available_fields, 'list')
        else:
            self.find_key_difference(mandatory_fields, available_fields)

    def find_key_difference(self, mandatory_fields, available_fields, path = "root"):
        """
        finds the key difference between two dictionary
        if the key present in both expected and available data the data validation will take place

        Args:
            mandatory_fields (dict): mandatory fields which should exist
            available_fields (dict): available data for validation
            path (str, optional): current data path
        """
        for key in mandatory_fields.keys():
            if key not in available_fields:
                print (path + " : " + key + " =>  as key not in fields list")
            else:
                self.check_for_valid_data(key, mandatory_fields, available_fields, path)


    def check_for_valid_format(self, format, list, path):
        """
        Validates the data based on type of data provided
        for the dictionary and list the validation performed differently
        choice of validation depends on type of format

        Args:
            format (dict, list): format to be validated
            list (list): list of data
            path (str): data path
        """
        if type(format) is dict:
            for item in list:
                self.find_key_difference(format, item, path)
        else:
            for item in list:
                self.check_for_valid_value(format, item)



    def check_for_valid_data(self, key, mandatory_fields, available_fields, path):
        """
        checks for the valid data in the available fields

        This will check the type of data is dict. If yes path is updated and validation continues
        This will handle validating list or dict or a normal string based on its type
        the value validation is done only when the key is present

        Args:
            key (str): key in the dictionary to be validated
            mandatory_fields (dict, list, str): field to be validated for
            available_fields (dict, list, str): available response fields to be validated
            path (str): current data path
        """
        if type(mandatory_fields) is not str:
            if path == "":
                path = key
            else:
                path = path + " -> " + key
        if type(mandatory_fields[key]) is dict:
            self.find_key_difference(
                mandatory_fields[key],
                available_fields[key],
                path
            )
        elif type(mandatory_fields[key]) is list and len(mandatory_fields[key]) == 1:
            self.check_for_valid_list(
                mandatory_fields[key][0],
                available_fields[key],
                path
            )
        else:
            self.check_for_valid_value(
                mandatory_fields[key],
                available_fields[key]
            )

    def check_for_valid_value(self, required_data, input_data):
        """
        Validated the data value for the format specified
        expected data can is a list or a RegEx

        Args:
            required_data (list, str): the data should be of this format or exist in list
            input_data (str): data available in the response
        
        Returns:
            void: no data
        """
        if required_data is None:
            return
        elif type(required_data) is list:
            if input_data in required_data:
                return;
            else:
                print('invalid data ' + str(input_data))
                exit()
        else:
            if re.search('^'+required_data+'$', str(input_data)):
                return
            else:
                print('data missmatch '+ str(input_data))
