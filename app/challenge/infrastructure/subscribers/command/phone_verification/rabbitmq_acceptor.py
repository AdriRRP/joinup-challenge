import json

from app.challenge.config import Config
from app.challenge.infrastructure.subscribers.rabbitmq_thread_subscriber import RabbitMQThreadSubscriber
from lib.challenge.phone_verification.application.accept.command.command import Command
from lib.challenge.phone_verification.application.accept.command.handler import Handler
from lib.shared.domain.bus.domain_event.subscriber import Subscriber


class RabbitPhoneVerificationAcceptor(RabbitMQThreadSubscriber):

    # Treat command handlers as subscriber
    class PhoneVerificationAcceptorSubscriber(Subscriber):

        @staticmethod
        def subscribed_to() -> list[str]:
            return ["accept.phone_verification.command"]

    def __init__(self, config: Config, handler: Handler):
        super().__init__(
            config,
            RabbitPhoneVerificationAcceptor.PhoneVerificationAcceptorSubscriber(),
            "challenge.phone_verification",
            "command_bus_exchange",
        )
        self._handler = handler

    def callback(self, channel, method, properties, body):
        message = json.loads(body)
        event = Command.new(
            message['data']['attributes']['code'],
        )
        self._handler.handle(event)
