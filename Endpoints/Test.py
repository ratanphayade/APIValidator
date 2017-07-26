from lib.Request import Request

class Test(Request):

    rules = {
        'method' : 'GET',
        'protocol' : 'https',
        'dns' : 'api.coupondunia.in',
        'path' : '/timestamp',
        'custom_status_header' : 'X-API-ErrorCode',
        'headers' : None,
        'validate_response' : True,
        'validate_result' : False,
        'response' : {
            'time' : '\d+',
        }
        # 'content_type' : 'application/json'
    }




