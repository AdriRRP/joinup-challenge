import json

from app.challenge.config import Config
from app.challenge.infrastructure.subscribers.rabbitmq_thread_subscriber import RabbitMQThreadSubscriber
from lib.challenge.email_verification.application.accept.command.command import Command
from lib.challenge.email_verification.application.accept.command.handler import Handler
from lib.shared.domain.bus.domain_event.subscriber import Subscriber


class RabbitEmailVerificationAcceptor(RabbitMQThreadSubscriber):

    # Treat command handlers as subscriber
    class EmailVerificationAcceptorSubscriber(Subscriber):

        @staticmethod
        def subscribed_to() -> list[str]:
            return ["accept.email_verification.command"]

    def __init__(self, config: Config, handler: Handler):
        super().__init__(
            config,
            RabbitEmailVerificationAcceptor.EmailVerificationAcceptorSubscriber(),
            "challenge.email_verification",
            "command_bus_exchange",
        )
        self._handler = handler

    def callback(self, channel, method, properties, body):
        message = json.loads(body)
        event = Command.new(
            message['data']['attributes']['code'],
        )
        self._handler.handle(event)
