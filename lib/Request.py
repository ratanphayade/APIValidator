from lib.Header import Header
import http.client

class Request(Header):
    """
    This class is responsible for request management

    It will take care of headers, payload, data format etc
    This will create a stream connection based on the protocol specified in the rules
    """
    _request_params = None
    """
    dict: holds all the rules mentioned under request part of rule
    """

    __connection = None
    """
    object: Holds the connection object which is created based on the type of protocol used
    """

    _configuration = None
    """
    dict: Collection of all basic configuration
    """
    _logger = None
    """
    object: Instance of logger
    """

    def __init__(self, configuration, logger, request_params):
        """
        Initializes the current request instance 
        and initialized the class variable with the curresponding data passed
        """
        self._request_params = request_params
        self._configuration = configuration
        self._logger = logger    
        super().__init__(self._request_params)    


    def init_request(self):
        """
        Initializes the request by creating a connection to DNS based on the protocol mentioned
        this will also initialize the necessory request parameters
        """
        if self._request_params['protocol'] == 'HTTPS':
            self.__connection = http.client.HTTPSConnection(self._request_params['dns'])
        else:
            self.__connection = http.client.HTTPConnection(self._request_params['dns'])
        self.init_request_params()


    def init_request_params(self):
        """
        Initialize the request params 
        which included handling payload, formating the data and adding custom header
        """
        self.format_request_headers()
        self.append_custom_headers()


    def create_request(self):
        """
        Creates te request for the given rule.
        Before creating all the data are formated which are required for the request

        Returns:
            object: connection instnace for the current DNS
        """
        self.init_request()
        try:
            self.__connection.request(
                self._request_params['method']
                , self._request_params['path']
                ,  self.payload
                , self.headers
            )
        except:
            print('Request failed : ' + self._request_params['method'] + ' ' + self._request_params['dns']+self._request_params['path'])
            exit()
        return self.__connection





