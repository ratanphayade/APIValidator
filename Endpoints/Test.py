from lib.RequestValidator import RequestValidator

class Test(RequestValidator):

    rules = {
        'request' : {
            'method' : 'GET',
            'protocol' : 'HTTPS',
            'dns' : 'api.coupondunia.in',
            'path' : '/timestamp',
            'headers' : {
                'custom_header': 'additional_header'
            },
            'content_type': None
        },
        'response':{
            'content_type': 'json', # json, xml
            'expected_response' : {
                    'timestamp' : '\d+',
            },
            'headers': {}
        }
        # 'content_type' : 'application/json'
    }


    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)

    def additional_header(self):
        return {
            'test':'test'
        }




