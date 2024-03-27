from __future__ import annotations

import configparser
import os


class Config:
    APP_CONFIG_PATH_ENV = 'APP_CONFIG_PATH'
    DEFAULT_CONFIG_PATH = '../../../../etc/app/challenge/user/config.ini'

    def __init__(self):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.
        """

        config_path = os.getenv(
            Config.APP_CONFIG_PATH_ENV,
            Config.DEFAULT_CONFIG_PATH
        )

        config = configparser.ConfigParser()
        config.read(config_path)
        self._config = config

    @staticmethod
    def new() -> Config:
        """
        Factory method to create new config object

        @return: instance of config object
        """

        config = Config()
        return config

    def get(self) -> configparser.ConfigParser:
        """
        Access to private config parser.

        @return: instance of inner config parser
        """
        return self._config
