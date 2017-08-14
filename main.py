#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import yaml
import logging
import logging.config
from endpoints.Test import Test


class APIValidator:

    __CONFIG_BASE_PATH = 'config/'

    __logger = None

    __configuration = {}

    def __init__(self):
        self.__configuration = self.load_configuration('main.conf')
        if not self.__configuration:
            print('Failed to load initial configuration')
            exit()
        self.initialize_logger()
        self.initialize_default_conf('headers')

    def load_configuration(self, _file_):
        """
        This will load the configuration specified by the file passed
        If the path exist then only the configuration is returned
        Configuration file should be in YAML format
        All the configuration are loaded from config folder

        Args:
            _file_: configuration file name to load.

        Returns:
            Dictionary format of configuration.
        """

        if os.path.exists(self.__CONFIG_BASE_PATH + _file_):
            with open(self.__CONFIG_BASE_PATH + _file_, 'rt') as conf:
                return yaml.safe_load(conf.read())
        return {}


    def initialize_default_conf(self, key):
        if key not in self.__configuration:
            return {}
        elif type(self.__configuration[key]) == str:
            self.__configuration[key] = self.load_configuration(
                self.__configuration[key]
            )
        elif type(self.__configuration[key]) != dict:
            print('invalid format for '+ key)
            exit()

    def initialize_logger(self):
        self.initialize_advance_logger()
        if not self.__logger:
            self.initialize_basic_logger()

    def initialize_basic_logger(self):
        logging.basicConfig(level=logging.DEBUG)
        self.__logger = logging.getLogger(__name__)

    def initialize_advance_logger(self):
        if 'logger' not in self.__configuration:
            return

        config = self.initialize_default_conf('logger')
        if config:
            logging.config.dictConfig(config)
            self.__logger = logging.getLogger('main')

    def execute(self):
        Test(self.__configuration, logging).run()


if __name__ == '__main__':
    APIValidator().execute()



