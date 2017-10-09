#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, getopt
import yaml, logging
import logging.config
import pkgutil, importlib
from endpoints import *

class APIValidator:
    """
    This class is responsible for loading initial setup.
    It loads the configurations requred for the validation
    It lists all the rules (or requests) to validate and manages the execution
    All the rules which will be validated should extend RequestValidator class

    Attributes:
        __CONFIG_BASE_PATH (str): Base path where all the configuration files can be found
        __logger (object): logger object which will be used app wide
        __configuration (dict): holds the general global configuration required for the execution

    """

    __CONFIG_BASE_PATH = 'config/'
    """
    str: Base path to the configuration files.

    It holds the base path to the location of the folder which contains 
    all the configuration files. This directory should atleast container 
    one main configuration file which is main.conf
    """

    __logger = None
    """
    Object: logger instnace 

    holds the logger instance valid throghout the application
    """

    __configuration = {}
    """
    dict: Dictionary of application configuration

    holds all the configurations for the application which can be used to define the application 
    it contains  configuration of request, response, header, logger etc
    """

    def __init__(self):
        """
        Initializes the APIValidator instance
        loads the default configuration defined in `main.conf`
        initializes the logger configuration if exist else creates a basic logger
        initializes header configurations in exist
        """
        self.__configuration = self.load_configuration('main.conf')

        if not self.__configuration:
            print('Failed to load initial configuration')
            exit()
        self.initialize_logger()
        """
        logger is been initialted based on the configuration provided 
        if the configuraiton is not provided in main.conf basic logger is configured
        """
        self.initialize_configuration('headers')
        """
        Initialize the header configuration for the current request
        this header configuration will be common accross all the request
        """

    def load_configuration(self, _file_):
        """
        This will load the configuration specified by the file passed
        If the path exist then only the configuration is returned
        Configuration file should be in YAML format
        The configuration file should be located in the base path specified

        Args:
            _file_: configuration file name to load.

        Returns:
            dict: Dictionary format of configuration.
        """

        if os.path.exists(self.__CONFIG_BASE_PATH + _file_):
            with open(self.__CONFIG_BASE_PATH + _file_, 'rt') as conf:
                return yaml.safe_load(conf.read())
        return {}


    def initialize_configuration(self, key):
        """
        The key will be with respect to the initial configuration file `main.py`
        Gonfiguration is loaded only if the given key has a reference to configuration file
        If the key has a configuration in form of dictionary then by default its loaded from base confif

        Args:
            key: key of configuration which has to be loaded.
        """
        if key not in self.__configuration:
            """
            No operation to perform if key is not present
            """
            return {}
        elif type(self.__configuration[key]) == str:
            """
            Load configuration from file if the reference to a file is given
            """
            self.__configuration[key] = self.load_configuration(
                self.__configuration[key]
            )
        elif type(self.__configuration[key]) != dict:
            """
            Configuration is invalid if its other then dictrinary format
            """
            print('invalid format for '+ key)
            exit()

    def initialize_logger(self):
        """
        This method will initialize the loggers based on the configuration specified in .conf file
        in case of absence of the configuration, it loads teh basic logger configuration
        """
        self.initialize_advance_logger()
        """
        Initializes the logger based on the configuration if configuration is specified
        """
        if not self.__logger:
            """
            Loads the basic logger configuration in case of logger configurations not found
            """
            self.initialize_basic_logger()

    def initialize_basic_logger(self):
        """
        This will be called when logger configuration is not found 
        this method will initialize the logger with the basic configuration
        """
        logging.basicConfig(level=logging.DEBUG)
        self.__logger = logging.getLogger(__name__)

    def initialize_advance_logger(self):
        """
        Logger is initialized based on the configuration specified
        in case of missing configuration the logger will not be initialized
        """
        if 'logger' not in self.__configuration:
            return

        config = self.initialize_configuration('logger')
        """
        Configuration is loaded from the file specified
        """
        if config:
            """
            If configuration is found, then logger is configured 
            """
            logging.config.dictConfig(config)
            self.__logger = logging.getLogger(__name__)

    def usage(self):
        print('python3 main.py [options]')
        exit()

    def add_argumet_filter(self, scripts):
        """
        Options are evaliated and based on which the updated list of tests are generated

        -r option will add the argument mentioned in the running list
        -x will eleminate the test from the running list

        Args:
            scripts (list): list of test to run by default

        Returns:
            updated running list of tests
        """
        try:
            opts, args = getopt.getopt(sys.argv[1:], "r:x:", ["run=", "exclude="])
        except getopt.GetoptError as err:
            print(err)
            self.usage()

        new_list = []
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.usage()
            elif opt in ('-r', '--run'):
                new_list.append(arg)
            elif opt in ('-x', '--exclude'):
                scripts.remove(arg)
        
        if new_list:
            return new_list
        else:
            return scripts
    

    def get_test_list(self):
        """
        Gives the list of test script to run

        The priority of section is as below:
            - This will default consider all the list 
            - The list is taken from the config
            - command line options are evaliated -r will run only that test -x will exclude the test from running config

        Returns:
            list of tests to run
        """
        self.initialize_configuration('tests')
        if 'tests' in self.__configuration:
            scripts = self.__configuration['tests']
        else:
            scripts = [name for _, name, _ in pkgutil.iter_modules(['endpoints'])]
        
        return self.add_argumet_filter(scripts)
    

    def execute(self):
        """
        Executes the rules from the list given and validated for the required content
        """
        test_list = self.get_test_list()
        if not test_list:
            print('No test scripts found')
            exit()
        for test in test_list:
            try:                
                getattr(globals()[test], test)(self.__configuration, logging).run()
            except:
                print('Nothoing like '+ test + ' found in endpoints')

if __name__ == '__main__':
    """
    Executes the validator if this file is executed
    Executes only when this file is been execited
    If this file in included the below code wont execute
    """
    APIValidator().execute()



