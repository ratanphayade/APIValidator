import validators
import json
import sys
from urllib.parse import urlencode

class BaseValidator:

    allowed_methods =  ['GET', 'POST']

    allowed_response_format = ['json', 'xml']

    def valid_endpoint(self, endpoint):
        if not validators.url(endpoint):
            raise Exception('Invalid endpoint '+ endpoint)
        return True

    def valid_method(self, method):  
        if not method in self.allowed_methods:
            raise Exception('Invalid method '+ method)
        return method

    def valid_response_format(self, response_format):
        return json.loads(json.dumps(response_format))

    def create_headers(self, headers):
        header = json.loads(json.dumps(headers))
        if header is None:
            return {}
        else:
            return header

    def create_post_body(self, rules):
        if 'content_type' not in rules:
            return ''
        elif rules['content_type'] == 'application/json':
            return json.loads(json.dumps(rules['body']))
        else:
            return urlencode(rules['body'])

    def get_text_encoding(self, rules):
        if 'encoding' not in rules:
            return "utf-8"
        else:
            return rules['encoding']

    def validate_response(self, rules, response):
        if 'validate_result' in rules and rules['validate_result']:
            print('validating result')
            self.result_validator(
                rules['response']
                , response.read().decode(
                    self.get_text_encoding(rules)
                )
            )
        elif 'validate_response' in rules and rules['validate_response']:
            print('validating response')            
            self.key_validator(
                rules['response']
                , response.read().decode(
                    self.get_text_encoding(rules)
                )
            )
        else:
            print('success')
            
    def result_validator(self, response_format, result_set):
        pass

    def key_validator(self, response_format, result_set):
        result = json.loads(result_set)
        self.find_key_difference(response_format, result)
        self.find_extra_key_difference(result, response_format)
        
    def find_key_difference(self, format, response, path = "root"):
        for k in format.keys():
            if k not in response:
                print (path + " : ")
                print(k + " as key not in response")
            else:
                if type(format[k]) is dict:
                    if path == "":
                        path = k
                    else:
                        path = path + "->" + k
                    find_key_difference(format[k],response[k], path)
                # else:
                #     if format[k] != response[k]:
                #         print path, ":"
                #         print " - ", k," : ", format[k]
                #         print " + ", k," : ", response[k] 

    def find_extra_key_difference(self, response, format, path = "root"):
        for k in response.keys():
            if k not in format:
                print (path + " : ")
                print(k + " as key not in format")
            else:
                if type(response[k]) is dict:
                    if path == "":
                        path = k
                    else:
                        path = path + "->" + k
                    find_extra_key_difference(response[k], format[k], path)
                # else:
                #     if format[k] != response[k]:
                #         print path, ":"
                #         print " - ", k," : ", format[k]
                #         print " + ", k," : ", response[k] 