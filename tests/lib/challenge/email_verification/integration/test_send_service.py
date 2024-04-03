import unittest

from lib.challenge.email_verification.application.accept.service import EmailVerificationAcceptor
from lib.challenge.email_verification.application.send.service import VerificationSender
from lib.challenge.email_verification.domain.domain_event.accepted import Accepted
from lib.challenge.email_verification.domain.domain_event.not_accepted import NotAccepted
from lib.challenge.email_verification.domain.domain_event.sent import Sent
from lib.challenge.email_verification.domain.verification import Verification
from lib.challenge.email_verification.infrastructure.repository.in_memory import InMemory
from lib.challenge.user.domain.email import Email
from lib.challenge.user.domain.id import Id
from lib.shared.domain.bus.domain_event.domain_event import DomainEvent
from lib.shared.domain.email_service import EmailService
from lib.shared.domain.value_object.uuid import Uuid
from lib.shared.domain.bus.domain_event.bus import Bus as EventBus


class TestVerificationSender(unittest.TestCase):
    test_verification = Verification.new(
        Uuid.new("a8f4f4f8-25e1-4a61-91d4-ec8975a2e580").ok_value,
        Id.new("6287aa63-ac02-4957-8424-efb5af11cb4a").ok_value,
        Email.new("first.user@mail.com").ok_value,
    )

    test_in_memory_verification_repository = InMemory.new([])

    class TestEventBus(EventBus):
        def __init__(self):
            self.events: list[DomainEvent] = []

        def publish(self, domain_event: DomainEvent):
            self.events.append(domain_event)

        def clear(self):
            self.events.clear()

    test_event_bus = TestEventBus()

    class TestEmailService(EmailService):
        def __init__(self):
            self.mails: list[dict] = []

        def send(self, email: str, body: str):
            self.mails.append({
                'email': email,
                'body': body,
            })

        def clear(self):
            self.mails.clear()

    test_email_service = TestEmailService()

    def test_accept(self):
        event_bus = TestVerificationSender.test_event_bus
        email_service = TestVerificationSender.test_email_service
        verification = TestVerificationSender.test_verification
        service = VerificationSender.new(
            email_service,
            event_bus,
            "http://localhost/api/v1/verification"
        )

        self.assertEqual(len(event_bus.events), 0)
        self.assertEqual(len(email_service.mails), 0)

        service.send(verification)

        self.assertEqual(len(event_bus.events), 1)
        self.assertEqual(len(email_service.mails), 1)

        event = event_bus.events.pop()
        mail = email_service.mails.pop()

        self.assertEqual(type(event).__name__, Sent.__name__)
        self.assertEqual(mail, {
            'email': verification.email(),
            'body': f"Click http://localhost/api/v1/verification/{verification.code()} to verify your email"
        })

        event_bus.clear()
        email_service.clear()


if __name__ == '__main__':
    unittest.main()
