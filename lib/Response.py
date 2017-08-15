from lib.Header import Header

class Response(Header):

    _response_params = None

    _configuration = None

    _logger = None

    def __init__(self, configuration, logger, response_params):
        self._response_params = response_params
        self._configuration = configuration
        self._logger = logger    
        super().__init__(self._response_params)
        

    def validate_response(self, response):
        print(response)
        self.validate_response_format(
            self._response_params['expected_response'], 
            response
        )