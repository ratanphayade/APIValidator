from lib.Header import Header

class Response(Header):

    __response_params = None

    _configuration = None

    _logger = None

    def __init__(self, configuration, logger, response_params):
        self.__response_params = response_params
        self._configuration = configuration
        self._logger = logger    
        

    def validate_response(self, response):
        print(response)
        self.check_for_matching_format(
            self.__response_params['expected_response'], 
            response
        )