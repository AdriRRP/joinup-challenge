import json

from app.challenge.config import Config
from app.challenge.infrastructure.subscribers.rabbitmq_thread_subscriber import RabbitMQThreadSubscriber
from lib.challenge.email_verification.application.create.subscriber import CreateEmailVerificationOnUserCreated
from lib.challenge.user.domain.domain_event.created import Created


class RabbitMQCreateEmailVerificationOnUserCreatedSubscriber(RabbitMQThreadSubscriber):

    def __init__(self, config: Config, service: CreateEmailVerificationOnUserCreated):
        super().__init__(
            config,
            service,
            "challenge.create_email_verification_on_user_created",
            "event_bus_exchange",
        )
        self._service = service

    def callback(self, channel, method, properties, body):
        message = json.loads(body)
        event = Created.new(
            message['data']['aggregateId'],
            message['data']['attributes']['name'],
            message['data']['attributes']['surname'],
            message['data']['attributes']['email'],
            message['data']['attributes']['phone'],
            message['data']['attributes']['hobbies'],
        )
        self._service.process(event)
