from lib.Request import Request
from lib.Response import Response
import json

class RequestValidator(Request):    

    _configuration = None

    _logger = None

    def __init__(self, configuration, logging):
        print('Validating '+ self.__class__.__name__)
        self._configuration = configuration
        self._logger = logging.getLogger(self.__class__.__name__)
        self.validate_rule(self.REQUIRED_ATTRIBUTES, self.rules)
        super().__init__(
            self._configuration, 
            self._logger, 
            self.rules['request']
        )


    def run(self):
        response = self.create_request().getresponse()        
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
        
