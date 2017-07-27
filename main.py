#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import yaml
import logging
import logging.config
from Endpoints.Test import Test


class APIValidator:

    _PATH = 'config/'

    logger = None

    configuration = {}

    def __init__(self):
        self.configuration = self.load_configuration('main.conf')
        if not self.configuration:
            print('Failed to load initial configuration')
            exit()
        self.initialize_logger()

    def load_configuration(self, _file_):
        """
        This is an example of Google style.

        Args:
            param1: This is the first param.
            param2: This is a second param.

        Returns:
            This is a description of what is returned.

        Raises:
            KeyError: Raises an exception.
        """

        if os.path.exists(self._PATH + _file_):
            with open(self._PATH + _file_, 'rt') as conf:
                return yaml.safe_load(conf.read())
        return {}

    def initialize_logger(self):
        self.initialize_advance_logger()
        if not self.logger:
            self.initialize_basic_logger()

    def initialize_basic_logger(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def initialize_advance_logger(self):
        if 'logger' not in self.configuration:
            return

        config = self.load_configuration(self.configuration['logger'])
        if config:
            logging.config.dictConfig(config)
            self.logger = logging.getLogger('main')

    def execute(self):
        Test().run()


if __name__ == '__main__':
    APIValidator().execute()



