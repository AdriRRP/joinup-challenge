import json

from app.challenge.config import Config
from app.challenge.infrastructure.subscribers.rabbitmq_thread_subscriber import RabbitMQThreadSubscriber
from lib.challenge.user.application.register.command.command import Command
from lib.challenge.user.application.register.command.handler import Handler
from lib.shared.domain.bus.domain_event.subscriber import Subscriber


class RabbitUserCreator(RabbitMQThreadSubscriber):

    # Treat command handlers as subscriber
    class UserCreatorSubscriber(Subscriber):

        @staticmethod
        def subscribed_to() -> list[str]:
            return ["create.user.command"]

    def __init__(self, config: Config, handler: Handler):
        super().__init__(
            config,
            RabbitUserCreator.UserCreatorSubscriber(),
            "challenge.user",
            "command_bus_exchange",
        )
        self._handler = handler

    def callback(self, channel, method, properties, body):
        message = json.loads(body)
        event = Command.new(
            message['data']['attributes']['id'],
            message['data']['attributes']['name'],
            message['data']['attributes']['surname'],
            message['data']['attributes']['email'],
            message['data']['attributes']['phone'],
            message['data']['attributes']['hobbies'],
        )
        self._handler.handle(event)
