import json

from app.challenge.config import Config
from app.challenge.infrastructure.subscribers.rabbitmq_thread_subscriber import RabbitMQThreadSubscriber
from lib.challenge.email_verification.domain.domain_event.accepted import Accepted
from lib.challenge.user.application.verify_email.subscriber import VerifyEmailOnEmailVerificationAccepted


class RabbitMQVerifyEmailOnEmailVerificationAcceptedSubscriber(RabbitMQThreadSubscriber):

    def __init__(self, config: Config, service: VerifyEmailOnEmailVerificationAccepted):
        super().__init__(
            config,
            service,
            "challenge.verify_email_on_email_verification_accepted",
            "event_bus_exchange",
        )
        self._service = service

    def callback(self, channel, method, properties, body):
        message = json.loads(body)
        event = Accepted.new(
            message['data']['aggregateId'],
            message['data']['attributes']['user_id'],
            message['data']['attributes']['email'],
        )
        self._service.process(event)
