from lib.Request import Request
from lib.Response import Response
from lib.Validator import Validator
import json

class RequestValidator(Validator):    

    _configuration = None

    _logger = None

    def __init__(self, configuration, logging):
        print('Validating '+ self.__class__.__name__)
        self._configuration = configuration
        self._logger = logging.getLogger(self.__class__.__name__)
        self.validate_request_params()


    def validate_request_params(self):
        Validator().validate_rule(self.REQUIRED_ATTRIBUTES, self.rules)



    def run(self):
        response = Request(
            self._configuration, 
            self._logger, 
            self.rules['request']
        ).create_request().getresponse()        
        Response(
            self._configuration, 
            self._logger, 
            self.rules['response']
        ).validate_response(
            json.loads(
                response.read().decode(
                    self._configuration['encoding']
                )
            )
        )
        print('complete')
        
