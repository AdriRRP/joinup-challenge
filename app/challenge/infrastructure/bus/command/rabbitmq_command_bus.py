from __future__ import annotations

import logging

import pika
from pika.exchange_type import ExchangeType
from app.challenge.config import Config
from lib.shared.domain.bus.command.bus import Bus
from lib.shared.domain.bus.command.command import Command

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class RabbitMQCommandBus(Bus):
    EXCHANGE_TYPE = ExchangeType.topic
    PUBLISH_INTERVAL = 1

    def __init__(self, conf: Config):
        self._credentials = pika.PlainCredentials(
            conf.get()['RABBITMQ']['user'],
            conf.get()['RABBITMQ']['pass'],
        )
        self._conn_params = pika.ConnectionParameters(
            host=conf.get()['RABBITMQ']['host'],
            port=conf.get()['RABBITMQ']['port'],
            credentials=self._credentials,
        )
        self._connection = pika.BlockingConnection(self._conn_params)
        self._channel = self._connection.channel()
        self._exchange_name = conf.get()['RABBITMQ']['command_bus_exchange']
        self._exchange = self._channel.exchange_declare(
            exchange=self._exchange_name,
            exchange_type='topic',
            passive=False,
            durable=True,
            auto_delete=False,
        )

    @staticmethod
    def new(config: Config) -> RabbitMQCommandBus:
        """
        Factory method to create new RabbitMQ event bus

        @return: instance of config object
        """

        command_bus = RabbitMQCommandBus(config)
        return command_bus

    def dispatch(self, command: Command):
        routing_key = command.command_name()
        content = command.serialize()

        print(f"Dispatching command ({routing_key}): {command.to_primitive()}")

        self._channel.basic_publish(
            exchange=self._exchange_name,
            routing_key=routing_key,
            body=content,
            properties=pika.BasicProperties(
                message_id=command.command_id(),
                content_type='application/json',
                content_encoding='utf-8',
                delivery_mode=1,
            ),
        )

