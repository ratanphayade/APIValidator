from lib.Request import Request
from lib.Response import Response
import json

class RequestValidator(Request):
    """
    This class will manage all the operation of a validation
    this is responsible for getting the response and sendting it for validation
    This will coordinate between request and response 
    """

    _configuration = None
    """
    dict: Collection of all basic configuration
    """

    _logger = None
    """
    object: Instance of logger
    """

    def __init__(self, configuration, logging):
        """
        Initializes the validation process for the current rule
        This will validate the rule for the minimum required data and its format
        Initializes the logger on the rule name to make it easy to debug

        Args:
            configuration (dict): basic application configuration
            logging (object): logger instance
        """
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
        """
        Runs the validation on current rule 
        """
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
        
