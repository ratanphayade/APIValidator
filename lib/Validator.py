from lib.Constants import Constants
import re

class Validator(Constants):

    def __init__(self):
        pass

    def check_for_matching_format(self, mandatory_fields, available_fields):
        if type(mandatory_fields) is list:
            self.check_for_valid_format(mandatory_fields[0], available_fields, 'list')
        else:
            self.find_key_difference(mandatory_fields, available_fields)

    def find_key_difference(self, mandatory_fields, available_fields, path = "root"):
        for key in mandatory_fields.keys():
            if key not in available_fields:
                print (path + " : " + key + " =>  as key not in fields list")
            else:
                self.check_for_valid_data(key, mandatory_fields, available_fields, path)


    def check_for_valid_format(self, format, list, path):
        if type(format) is dict:
            for item in list:
                self.find_key_difference(format, item, path)
        else:
            for item in list:
                self.check_for_valid_value(format, item)



    def check_for_valid_data(self, key, mandatory_fields, available_fields, path):
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
            # if self.__class__.__name__ == 'Response':
            #     print(type(available_fields))
            #     exit()
            self.check_for_valid_value(
                mandatory_fields[key],
                available_fields[key]
            )

    def check_for_valid_value(self, required_data, input_data):
        if required_data is None:
            return
        elif type(required_data) is list:
            if input_data in required_data:
                return;
            else:
                print('invalid data ' + input_data)
                exit()
        else:
            if re.search('^'+required_data+'$', str(input_data)):
                return
            else:
                print('data missmatch '+ input_data)
