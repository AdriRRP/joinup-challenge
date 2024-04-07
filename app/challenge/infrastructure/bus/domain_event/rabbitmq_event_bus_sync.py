from __future__ import annotations

import logging
from typing import Optional

import pika
from pika.exchange_type import ExchangeType
from app.challenge.config import Config
from lib.shared.domain.bus.domain_event.bus import Bus
from lib.shared.domain.bus.domain_event.domain_event import DomainEvent

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class RabbitMQEventBus(Bus):
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
        self._exchange_name = conf.get()['RABBITMQ']['event_bus_exchange']
        self._exchange = self._channel.exchange_declare(
            exchange=self._exchange_name,
            exchange_type='topic',
            passive=False,
            durable=True,
            auto_delete=False,
        )

    @staticmethod
    def new(config: Config) -> RabbitMQEventBus:
        """
        Factory method to create new RabbitMQ event bus

        @return: instance of config object
        """

        event_bus = RabbitMQEventBus(config)
        return event_bus

    def publish(self, domain_event: DomainEvent):
        routing_key = domain_event.name()
        content = domain_event.serialize()

        self._channel.basic_publish(
            exchange=self._exchange_name,
            routing_key=routing_key,
            body=content,
            properties=pika.BasicProperties(
                message_id=domain_event.event_id(),
                content_type='application/json',
                content_encoding='utf-8',
                delivery_mode=1,
            ),
        )