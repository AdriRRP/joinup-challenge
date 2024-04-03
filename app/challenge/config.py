from __future__ import annotations

import configparser
import os


class Config:
    APP_CONFIG_PATH_ENV = 'APP_CONFIG_PATH'
    DEFAULT_CONFIG_PATH = '../../../../etc/app/challenge/config.ini'

    # Mongo env vars
    APP_MONGO_URI_ENV = 'APP_MONGO_URI'
    APP_MONGO_DATABASE_ENV = 'APP_MONGO_DATABASE'
    APP_MONGO_USER_ENV = 'APP_MONGO_USER'
    APP_MONGO_PASS_ENV = 'APP_MONGO_PASS'

    # Challenge env vars
    APP_CHALLENGE_USER_COLLECTION_ENV = 'APP_CHALLENGE_USER_COLLECTION'
    APP_CHALLENGE_EMAIL_VERIFICATION_COLLECTION_ENV = 'APP_CHALLENGE_EMAIL_VERIFICATION_COLLECTION'
    APP_CHALLENGE_PHONE_VERIFICATION_COLLECTION_ENV = 'APP_CHALLENGE_PHONE_VERIFICATION_COLLECTION'

    # RabbitMQ env vars
    APP_RABBITMQ_HOST_ENV = 'APP_RABBITMQ_HOST'
    APP_RABBITMQ_PORT_ENV = 'APP_RABBITMQ_PORT'
    APP_RABBITMQ_USER_ENV = 'APP_RABBITMQ_USER'
    APP_RABBITMQ_PASS_ENV = 'APP_RABBITMQ_PASS'
    APP_RABBITMQ_EVENT_BUS_EXCHANGE_ENV = 'APP_RABBITMQ_EVENT_BUS_EXCHANGE'
    APP_RABBITMQ_COMMAND_BUS_EXCHANGE_ENV = 'APP_RABBITMQ_COMMAND_BUS_EXCHANGE'

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

        self._data = {
            "MONGO": {
                "uri": os.getenv(
                    Config.APP_MONGO_URI_ENV,
                    config['MONGO']['uri']
                ),
                "database": os.getenv(
                    Config.APP_MONGO_DATABASE_ENV,
                    config['MONGO']['database']
                ),
                "user": os.getenv(
                    Config.APP_MONGO_USER_ENV,
                    config['MONGO']['user']
                ),
                "pass": os.getenv(
                    Config.APP_MONGO_PASS_ENV,
                    config['MONGO']['pass']
                ),
            },
            "CHALLENGE": {
                "user_collection": os.getenv(
                    Config.APP_CHALLENGE_USER_COLLECTION_ENV,
                    config['CHALLENGE']['user_collection']
                ),
                "email_verification_collection": os.getenv(
                    Config.APP_CHALLENGE_EMAIL_VERIFICATION_COLLECTION_ENV,
                    config['CHALLENGE']['email_verification_collection']
                ),
                "phone_verification_collection": os.getenv(
                    Config.APP_CHALLENGE_PHONE_VERIFICATION_COLLECTION_ENV,
                    config['CHALLENGE']['phone_verification_collection']
                ),
            },
            "RABBITMQ": {
                "host": os.getenv(
                    Config.APP_RABBITMQ_HOST_ENV,
                    config['RABBITMQ']['host']
                ),
                "port": os.getenv(
                    Config.APP_RABBITMQ_PORT_ENV,
                    config['RABBITMQ']['port']
                ),
                "user": os.getenv(
                    Config.APP_RABBITMQ_USER_ENV,
                    config['RABBITMQ']['user']
                ),
                "pass": os.getenv(
                    Config.APP_RABBITMQ_PASS_ENV,
                    config['RABBITMQ']['pass']
                ),
                "event_bus_exchange": os.getenv(
                    Config.APP_RABBITMQ_EVENT_BUS_EXCHANGE_ENV,
                    config['RABBITMQ']['event_bus_exchange']
                ),
                "command_bus_exchange": os.getenv(
                    Config.APP_RABBITMQ_COMMAND_BUS_EXCHANGE_ENV,
                    config['RABBITMQ']['command_bus_exchange']
                ),
            },
        }

    @staticmethod
    def new() -> Config:
        """
        Factory method to create new config object

        @return: instance of config object
        """

        config = Config()
        return config

    def get(self) -> dict:
        """
        Access to private config parser.

        @return: instance of inner config parser
        """
        return self._data
