from lib.Header import Header
import http.client

class Request(Header):

    __request_params = None

    __connection = None

    _configuration = None

    _logger = None

    def __init__(self, configuration, logger, request_params):
        self.__request_params = request_params
        self._configuration = configuration
        self._logger = logger        


    def init_request(self):
        if self.__request_params['protocol'] == 'HTTPS':
            self.__connection = http.client.HTTPSConnection(self.__request_params['dns'])
        else:
            self.__connection = http.client.HTTPConnection(self.__request_params['dns'])
        self.init_request_params()


    def init_request_params(self):
        self.format_request_headers()
        self.append_custom_headers()


    def create_request(self):
        self.init_request()
        try:
            self.__connection.request(self.__request_params['method'], self.__request_params['path'],  self.payload, self.headers)
        except:
            print('Request failed : ' + self.__request_params['method'] + ' ' + self.__request_params['dns']+self.__request_params['path'])
            exit()
        return self.__connection





