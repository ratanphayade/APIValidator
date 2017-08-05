from lib.RequestValidator import RequestValidator

class Test(RequestValidator):

    rules = {
        'request' : {
            'method' : 'GET',
            'protocol' : 'HTTP',
            'dns' : 'local.in',
            'path' : '/partner/public/timestamp',
            'headers' : None,
            'content_type': None
        },
        'response':{
            'content_type': 'json', # json, xml
            'expected_response' : [ # for response list, for result dict
                {
                    'timestamp' : '\d+',
                }
            ]
        }
        # 'content_type' : 'application/json'
    }


    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)





