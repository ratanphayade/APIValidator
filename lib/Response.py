from lib.Header import Header

class Response(Header):
    """
    This class is responsible for response management

    It will take care of headers, response data and its format
    The response data will be validated here against the format specified 
    """

    _response_params = None
    """
    dict: holds all the rules mentioned under response part of rule
    """

    _configuration = None
    """
    dict: Collection of all basic configuration
    """

    _logger = None
    """
    object: Instance of logger
    """

    def __init__(self, configuration, logger, response_params):
        """
        Initializes the current request instance 
        and initialized the class variable with the curresponding data passed
        """
        self._response_params = response_params
        self._configuration = configuration
        self._logger = logger    
        super().__init__(self._response_params)
        

    def validate_response(self, response):
        """
        Validates the response passed based on the response configuration in rules

        Args:
            response (str): response of the endpoint in string format         
        """
        print(response)
        self.validate_response_format(
            self._response_params['expected_response'], 
            response
        )