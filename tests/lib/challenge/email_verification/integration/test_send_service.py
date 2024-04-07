import unittest

from lib.challenge.phone_verification.application.send.service import VerificationSender
from lib.challenge.phone_verification.domain.domain_event.sent import Sent
from lib.challenge.phone_verification.domain.verification import Verification
from lib.challenge.phone_verification.infrastructure.repository.in_memory import InMemory
from lib.challenge.user.domain.phone import Phone
from lib.challenge.user.domain.id import Id
from lib.shared.domain.bus.domain_event.domain_event import DomainEvent
from lib.shared.domain.sms_service import SmsService
from lib.shared.domain.value_object.uuid import Uuid
from lib.shared.domain.bus.domain_event.bus import Bus as EventBus


class TestVerificationSender(unittest.TestCase):
    test_verification = Verification.new(
        Uuid.new("a8f4f4f8-25e1-4a61-91d4-ec8975a2e580").ok_value,
        Id.new("6287aa63-ac02-4957-8424-efb5af11cb4a").ok_value,
        Phone.new("+34 666 666 001").ok_value,
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

    class TestPhoneService(SmsService):
        def __init__(self):
            self.mails: list[dict] = []

        def send(self, phone: str, body: str):
            self.mails.append({
                'phone': phone,
                'body': body,
            })

        def clear(self):
            self.mails.clear()

    test_phone_service = TestPhoneService()

    def test_accept(self):
        event_bus = TestVerificationSender.test_event_bus
        sms_service = TestVerificationSender.test_phone_service
        verification = TestVerificationSender.test_verification
        service = VerificationSender.new(
            sms_service,
            event_bus,
            "http://localhost/api/v1/verification"
        )

        self.assertEqual(len(event_bus.events), 0)
        self.assertEqual(len(sms_service.mails), 0)

        service.send(verification)

        self.assertEqual(len(event_bus.events), 1)
        self.assertEqual(len(sms_service.mails), 1)

        event = event_bus.events.pop()
        mail = sms_service.mails.pop()

        self.assertEqual(type(event).__name__, Sent.__name__)
        self.assertEqual(mail, {
            'phone': verification.phone(),
            'body': f"Click http://localhost/api/v1/verification/{verification.code()} to verify your phone"
        })

        event_bus.clear()
        sms_service.clear()


if __name__ == '__main__':
    unittest.main()
