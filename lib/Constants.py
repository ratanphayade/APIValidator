class Constants(object):
    """
    Holds all the constants used in the application
    it has all the valid data sets and formats
    All default are mentioned here
    """
    ALLOWED_METHODS = ['GET', 'POST']
    """
    list: list of allowed request method types
    """

    ALLOWED_PROTOCOLS = ['HTTP', 'HTTPS']
    """
    list: list of allowed request types
    """

    ALLOWED_RESPONSE_TYPES = ['json', 'xml']
    """
    list: list of supported response type for validation
    """

    CONTENT_TYPES = {
        'json' : 'application/json',
        'x-www-form-urlencoded' : 'application/x-www-form-urlencoded'
    }
    """
    dict: dictionaty of data type to content type
    """

    DEFAULT_CONTENT_TYPE = 'json'
    """
    str: default content type to consider when not specified
    """

    DEFAULT_RESPONSE_FORMAT = 'json'
    """
    str: default response type to consider when not specified
    """

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
    """
    dict: basic rule which should be present
    """


