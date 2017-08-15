#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import yaml
import logging
import logging.config
from endpoints.Test import Test


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

    def execute(self):
        """
        Executes the rules from the list given and validated for the required content
        """
        Test(self.__configuration, logging).run()


if __name__ == '__main__':
    """
    Executes the validator if this file is executed
    Executes only when this file is been execited
    If this file in included the below code wont execute
    """
    APIValidator().execute()



