from lib.Header import Header
import http.client

class Request(Header):

    _request_params = None

    __connection = None

    _configuration = None

    _logger = None


    def __init__(self, configuration, logger, request_params):
        self._request_params = request_params
        self._configuration = configuration
        self._logger = logger    
        super().__init__(self._request_params)    


    def init_request(self):
        if self._request_params['protocol'] == 'HTTPS':
            self.__connection = http.client.HTTPSConnection(self._request_params['dns'])
        else:
            self.__connection = http.client.HTTPConnection(self._request_params['dns'])
        self.init_request_params()


    def init_request_params(self):
        self.format_request_headers()
        self.append_custom_headers()


    def create_request(self):
        self.init_request()
        try:
            self.__connection.request(self._request_params['method'], self._request_params['path'],  self.payload, self.headers)
        except:
            print('Request failed : ' + self._request_params['method'] + ' ' + self._request_params['dns']+self._request_params['path'])
            exit()
        return self.__connection





