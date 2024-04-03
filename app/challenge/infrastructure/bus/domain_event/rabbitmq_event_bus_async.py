from __future__ import annotations

import functools
import logging
import threading
import time
from typing import Optional

import pika
from pika.exchange_type import ExchangeType
from app.challenge.config import Config
from lib.shared.domain.bus.domain_event.bus import Bus
from lib.shared.domain.bus.domain_event.domain_event import DomainEvent

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class RabbitMQEventBus(threading.Thread, Bus):
    EXCHANGE_TYPE = ExchangeType.topic
    PUBLISH_INTERVAL = 1

    def __init__(self, conf: Config):
        super().__init__()
        self.setDaemon(True)

        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

        # Read config values
        self._user = conf.get()['RABBITMQ']['user']
        self._pass = conf.get()['RABBITMQ']['pass']
        self._host = conf.get()['RABBITMQ']['host']
        self._port = conf.get()['RABBITMQ']['port']
        self._exchange_name = conf.get()['RABBITMQ']['event_bus_exchange']

        # Helper params
        self._connection = None
        self._channel = None
        self._exchange = None

        self._deliveries = None
        self._acked = None
        self._nacked = None
        self._message_number = None

        self._stopping = False

        # Connection params
        self._credentials = pika.PlainCredentials(self._user, self._pass)
        self._conn_params = pika.ConnectionParameters(host=self._host, port=self._port, credentials=self._credentials)

        self._exchange_ready = False

        # Initialize
        self.start()

    @staticmethod
    def new(config: Config) -> RabbitMQEventBus:
        """
        Factory method to create new RabbitMQ event bus

        @return: instance of config object
        """

        event_bus = RabbitMQEventBus(config)
        return event_bus

    def connect(self):
        LOGGER.info(f"Connecting to {self._host}:{self._port}")
        connection = pika.SelectConnection(
            parameters=self._conn_params,
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
        )
        return connection

    def on_connection_open(self, _unused_connection):
        LOGGER.info('Connection opened')
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        LOGGER.error("Connection open failed, reopening in 5 seconds: {err}")
        self._connection.ioloop.call_later(5, self._connection.ioloop.stop)

    def on_connection_closed(self, _unused_connection, reason):
        self._channel = None
        if self._stopping:
            self._connection.ioloop.stop()
        else:
            LOGGER.warning(f"Connection closed, reopening in 5 seconds: {reason}")
            self._connection.ioloop.call_later(5, self._connection.ioloop.stop)

    def open_channel(self):
        LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        LOGGER.info('Channel opened')
        self._channel = channel
        self._channel.add_on_close_callback(self.on_channel_closed)
        self.setup_exchange()

    def on_channel_closed(self, channel, reason):
        LOGGER.warning(f"Channel {channel} was closed: {reason}")
        self._channel = None
        if not self._stopping:
            self._connection.close()

    def setup_exchange(self):
        LOGGER.info(f"Declaring exchange {self._exchange_name}")
        cb = functools.partial(
            self.on_exchange_declareok, userdata=self._exchange_name)
        self._exchange = self._channel.exchange_declare(
            exchange=self._exchange_name,
            exchange_type=self.EXCHANGE_TYPE,
            passive=False,
            durable=True,
            auto_delete=False,
            callback=cb
        )

    def on_exchange_declareok(self, _unused_frame, userdata):
        LOGGER.info(f"Exchange declared: {userdata}")
        self._exchange_ready = True
        LOGGER.info('Issuing Confirm.Select RPC command')
        self._channel.confirm_delivery(self.on_delivery_confirmation)

    def on_delivery_confirmation(self, method_frame):
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        ack_multiple = method_frame.method.multiple
        delivery_tag = method_frame.method.delivery_tag

        LOGGER.info(f"Received {confirmation_type} for delivery tag: {delivery_tag} (multiple: {ack_multiple})")

        if confirmation_type == 'ack':
            self._acked += 1
        elif confirmation_type == 'nack':
            self._nacked += 1

        del self._deliveries[delivery_tag]

        if ack_multiple:
            for tmp_tag in list(self._deliveries.keys()):
                if tmp_tag <= delivery_tag:
                    self._acked += 1
                    del self._deliveries[tmp_tag]
        """
        NOTE: at some point you would check self._deliveries for stale
        entries and decide to attempt re-delivery
        """

        LOGGER.info(
            f"Published {self._message_number} messages, {len(self._deliveries)} have yet to be confirmed, "
            f"{self._acked,} were acked and {self._nacked} were nacked"
        )

    def publish(self, domain_event: DomainEvent):
        while not self._exchange_ready:
            LOGGER.info(f"Waiting for exchange ready")
            time.sleep(1)

            cb = functools.partial(self.publish_message,
                                   domain_event=domain_event)
            self._connection.ioloop.call_later(self.PUBLISH_INTERVAL, cb)

    def publish_message(self, domain_event: DomainEvent):

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
            )
        )

        self._message_number += 1
        self._deliveries[self._message_number] = True
        LOGGER.info(f"Published message # {self._message_number}")

    def start(self):
        super().start()
        self._connection = self.connect()
        self._connection.ioloop.start()

