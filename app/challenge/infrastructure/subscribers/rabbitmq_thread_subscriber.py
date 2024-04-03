import functools
import logging
import threading
from abc import ABCMeta, abstractmethod

from app.challenge.config import Config
from lib.shared.domain.bus.domain_event.subscriber import Subscriber
from pika.exchange_type import ExchangeType
import pika

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class RabbitMQThreadSubscriber(threading.Thread, metaclass=ABCMeta):
    EXCHANGE_TYPE = ExchangeType.topic
    PUBLISH_INTERVAL = 1

    def __init__(self, conf: Config, subscriber: Subscriber, queue: str, exchange_key: str):
        super().__init__()

        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

        self._subscriber = subscriber

        # Read config values
        self._user = conf.get()['RABBITMQ']['user']
        self._pass = conf.get()['RABBITMQ']['pass']
        self._host = conf.get()['RABBITMQ']['host']
        self._port = conf.get()['RABBITMQ']['port']
        self._exchange_name = conf.get()['RABBITMQ'][exchange_key]
        self._queue = queue

        # Helper params
        self._connection = None
        self._channel = None
        self._exchange = None
        self.should_reconnect = False

        self.was_consuming = False

        self._closing = False
        self._consumer_tag = None
        self._consuming = False
        # In production, experiment with higher prefetch values
        # for higher consumer throughput
        self._prefetch_count = 1

        # Connection params
        self._credentials = pika.PlainCredentials(self._user, self._pass)
        self._conn_params = pika.ConnectionParameters(host=self._host, port=self._port, credentials=self._credentials)

    def connect(self):
        LOGGER.info(f"Connecting to {self._host}:{self._port}")
        connection = pika.SelectConnection(
            parameters=self._conn_params,
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
        )
        return connection

    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            LOGGER.info('Connection is closing or already closed')
        else:
            LOGGER.info('Closing connection')
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        LOGGER.info('Connection opened')
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        LOGGER.error("Connection open failed, reopening in 5 seconds: {err}")
        self._connection.ioloop.call_later(5, self._connection.ioloop.stop)

    def on_connection_closed(self, _unused_connection, reason):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            LOGGER.warning(f"Connection closed, reconnect necessary: {reason}")
            self.reconnect()

    def reconnect(self):
        self.should_reconnect = True
        self.stop()

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
        self.close_connection()

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
        self.setup_queue()

    def setup_queue(self):
        LOGGER.info(f"Declaring queue {self._queue}")
        self._channel.queue_declare(queue=self._queue, callback=self.on_queue_declareok)

    def on_queue_declareok(self, _unused_frame):
        for routing_key in self._subscriber.subscribed_to():
            LOGGER.info(f"Binding {self._exchange_name} to {self._queue} with {routing_key}")
            self._channel.queue_bind(
                self._queue,
                self._exchange_name,
                routing_key=routing_key,
                callback=self.on_bindok)

    def on_bindok(self, _unused_frame):
        LOGGER.info(f"Queue bound: {self._queue}")
        self.set_qos()

    def set_qos(self):
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        LOGGER.info(f"QOS set to: {self._prefetch_count}")
        self.start_consuming()

    def start_consuming(self):
        LOGGER.info("Issuing consumer related RPC commands")
        LOGGER.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

        self._consumer_tag = self._channel.basic_consume(
            queue=self._queue,
            on_message_callback=self.on_message,
        )
        self.was_consuming = True
        self._consuming = True

    def on_consumer_cancelled(self, method_frame):
        LOGGER.info(f"Consumer was cancelled remotely, shutting down: {method_frame}")
        if self._channel:
            self._channel.close()

    def on_message(self, channel, basic_deliver, properties, body):
        LOGGER.info(f"Received message # {basic_deliver.delivery_tag} from {properties.app_id}: {body}")
        try:
            self.callback(channel, basic_deliver, properties, body)
        except Exception as e:
            LOGGER.error(f"Error processing message: {e}")
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        LOGGER.info(f"Acknowledging message {delivery_tag}")
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        if self._channel:
            LOGGER.info("Sending a Basic.Cancel RPC command to RabbitMQ")
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        self._consuming = False
        LOGGER.info(
            'RabbitMQ acknowledged the cancellation of the consumer: %s',
            userdata)
        self.close_channel()

    def close_channel(self):
        LOGGER.info("Closing the channel")
        self._channel.close()

    @abstractmethod
    def callback(self, channel, method, properties, body):
        pass

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        if not self._closing:
            self._closing = True
            LOGGER.info('Stopping')
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            LOGGER.info('Stopped')