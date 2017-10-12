# APIValidator
Purpose of this project to to create a framework which can be used validate api by giving flexibility to validate different types of request types and response formats


#Scope
Maintaining a constant response while developping and bit difficult task. Especially when you have to take care of multiple endpoints. This project will solve the issue of validating the response with every development cycle.

The `APIValidator` will take simple set of rules associated with each request and validate the response accordingly 

#Installation

Start by cloning the repo.

```
$ git clone https://github.com/ratanphayade/APIValidator.git
```

run the below command to install dependencies

```
pip3 install yaml
```

#Configuration

All the configuration can be found in conf directory. Configuration should be in valid YAML format.

- main.conf

This is a mandatory configuration which will be loaded at the start.

This also contains reference to the multiple configuration files.
```
logger: logger.conf
headers: header.conf
tests: run.conf
```

- logger.conf

If `logger` will have the logging configuration details. This can be used to constomize the logs. If not specified default format will be used.

- headers.conf

This can be used to set a common headers to all the requests. Its a simple list of data which has to sent in headers.

- tests.conf

This will contain the list of request rule files which has to be tested by default.

#Writing Rules

- All the rules file is kept in endpoint directory. 
- All class name should share the name same as the file name.
- All classes should extend `RequestValidator` from `from lib.RequestValidator import RequestValidator`.
- All Classes should have constructor calling `super().__init__(configuration, logger)`.
- Rules should be writen in `JSON` format.

rules variable will hold the rules and it has 2 sections.
    - Request
    - Response

```
    rules = {
        'request' : {
            'method' : 'GET',
            'protocol' : 'HTTPS',
            'dns' : '<dns>',
            'path' : '<path>',
            'headers' : {
                'custom_header': '<function_name>'
            },
            'content_type': None,
            #payload : {}
        },
        'response':{
            'content_type': 'json', # json
            'expected_response' : {
                    'timestamp' : '\d+',
            },
            'headers': {}
        }
    }
```

##Request

- `method` : Here is request method. it can be either GET or POST. based on the method there can be few fields in the rules.
- `protocal` : This can be HTTP or HTTPS
- `dns` :  Domain name where the API is hosted
- `path` : URL path of the endpoint requesting
- `content_type` : It will be `None` for `GET` requests and for `POST` reuqest it should tell the `payload` type
- `payload` : Its valid only for `POST` requests. It will contait the post data in `JSON` fromat
- `headers` : If at all any headers to be added, then that should go here. this will be in a `JSON` format representing all the additional headers for the request. if any computation is required for the header then you can use `custom_header` inside the `headers` specifying the method name implimented in the rules and the methods return type should be `dict`. All the headers will be added to the request.

##Response

- `content_type` : It will specify the reposne data type. For now its only `JSON`
- `headers` : [TODO] Will list all the headers which has to be validated for for response.
- `expected_response` : Will contain the sample response format afainst which the API response has to be validated. 


###Writing Response validation format

1. The respose format can only validate for the required keys. In this case `expected_response` will look like below:
```
{
    'timestamp' : None,
    'type': None
}
```

2. The Response format shold also check for the data. In this case `expected_response` will look like below:
```
{
    'timestamp' : '\d+',
    'type' : ['TIME', 'DATE'],
}
```
The data here can be in the `RegEx` format in the format is known. If the data should be one which is known then we can give a list of possible data.

3. The Response is an array of Objects. In this case `expected_response` will look like below:
```
[
    {
        'timestamp' : '\d+',
    }
]
```
Only one element sample is needed to validate the all the array elements.


#Running the Test

To execute the sctipt run the command:
```
python3 mian.py
```

##Running all the test
If the `tests.conf` doesn't exist then all the rules will get executed.

##Running only few tests 
If have to run only certain number of tests repeatedly then we can used `tests.conf` and specify the list of rules to execute.

##Run Specific test
We can also use the command options to execute selected test or not execute selected test. 
- Options 
    `-r | --run` can be used to specify the rule to execute.
    `-x | '--exclude'` can be used to exclude a rule from the list.
    

#TODO
- Add Support to validate the JSON reponse if it just contains the list of strings.
- Support for XML reponse validation.



