import json

from app.challenge.config import Config
from app.challenge.infrastructure.subscribers.rabbitmq_thread_subscriber import RabbitMQThreadSubscriber
from lib.challenge.email_verification.application.send.subscriber import SendVerificationMailOnEmailVerificationCreated
from lib.challenge.email_verification.domain.domain_event.created import Created


class RabbitMQSendVerificationMailOnEmailVerificationCreatedSubscriber(RabbitMQThreadSubscriber):

    def __init__(self, config: Config, service: SendVerificationMailOnEmailVerificationCreated):
        super().__init__(
            config,
            service,
            "challenge.send_verification_mail_on_email_verification_created",
            "event_bus_exchange",
        )
        self._service = service

    def callback(self, channel, method, properties, body):
        message = json.loads(body)
        event = Created.new(
            message['data']['aggregateId'],
            message['data']['attributes']['user_id'],
            message['data']['attributes']['email'],
        )
        self._service.process(event)
