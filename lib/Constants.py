
class Constants():

    ALLOWED_METHODS = ['GET', 'POST']

    ALLOWED_PROTOCOLS = ['HTTP', 'HTTPS']

    ALLOWED_RESPONSE_TYPES = ['json', 'xml']

    CONTENT_TYPES = {
        'json' : 'application/json',
        'x-www-form-urlencoded' : 'application/x-www-form-urlencoded'
    }

    DEFAULTS_RESPONSE_FORMAT = 'json'

    REQUIRED_ATTRIBUTES = {
        'request':{                         # request attributes
            'dns' : '\S+',                  # host
            'path' : '\S+',                 # request URI
            'method' : ALLOWED_METHODS,     # GET, POST
            'protocol' : ALLOWED_PROTOCOLS, # http , https
            'headers' : None                # header class
        },
        'response': {                       # response attributes
            'expected_response' : None      # dict or list based on validation type
        }
    }


