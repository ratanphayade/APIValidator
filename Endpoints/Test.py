from lib.RequestValidator import RequestValidator

class Test(RequestValidator):

    rules = {
        'request' : {
            'method' : 'GET',
            'protocol' : 'HTTPS',
            'dns' : 'api.coupondunia.in',
            'path' : '/timestamp',
            'headers' : None,
            'content_type': None
        },
        'response':{
            'content_type': 'json', # json, xml
            'expected_response' : {
                    'timestamp' : '\d+',
            }
        }
        # 'content_type' : 'application/json'
    }


    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)





