from lib.Validator import Validator
import http.client

class Request:

    __name = None

    dns = None

    path = None

    headers = {}

    method = None

    payload = ''

    validator = None  

    protocol = None  
    
    def __init__(self):
        self.validator = Validator()
        self.__name = self.__class__.__name__
        print('Validating '+ self.__name)
        self.validate_request_params()

        
    def validate_request_params(self):        
        if self.validator.valid_endpoint(self.rules['protocol'] + '://' + self.rules['dns'] + self.rules['path']):
            self.protocol = self.rules['protocol']
            self.dns = self.rules['dns']
            self.path = self.rules['path']
        self.method = self.validator.valid_method(self.rules['method'])
        self.payload = self.validator.create_post_body(self.rules)
        self.headers = self.validator.create_headers(self.rules['headers'])
        self.validateResponse = self.rules['validate_response']
        self.validateResult = self.rules['validate_result']
        self.response = self.validator.valid_response_format(self.rules['response'])

    def run(self):
        if(self.protocol == 'https'):
            conn = http.client.HTTPSConnection(self.dns)
        else:
            conn = http.client.HTTPConnection(self.dns)

        try:
            conn.request(self.method, self.path,  self.payload, self.headers)
        except HTTPException:
            print('Request failed : ' + self.method + ' ' + self.rules['dns']+self.path)
            sys.exit()
        return self.validator.validate_response(
            self.rules, conn.getresponse()
        )



    
    