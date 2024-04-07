import unittest

from lib.challenge.phone_verification.application.accept.service import PhoneVerificationAcceptor
from lib.challenge.phone_verification.domain.domain_event.accepted import Accepted
from lib.challenge.phone_verification.domain.domain_event.not_accepted import NotAccepted
from lib.challenge.phone_verification.domain.verification import Verification
from lib.challenge.phone_verification.infrastructure.repository.in_memory import InMemory
from lib.challenge.user.domain.phone import Phone
from lib.challenge.user.domain.id import Id
from lib.shared.domain.bus.domain_event.domain_event import DomainEvent
from lib.shared.domain.value_object.uuid import Uuid
from lib.shared.domain.bus.domain_event.bus import Bus as EventBus


class TestVerificationAcceptor(unittest.TestCase):
    test_verification = Verification.new(
        Uuid.new("a8f4f4f8-25e1-4a61-91d4-ec8975a2e580").ok_value,
        Id.new("6287aa63-ac02-4957-8424-efb5af11cb4a").ok_value,
        Phone.new("+34 666 666 001").ok_value,
    )

    test_in_memory_verification_repository = InMemory.new([test_verification])

    class TestEventBus(EventBus):
        def __init__(self):
            self.events: list[DomainEvent] = []

        def publish(self, domain_event: DomainEvent):
            self.events.append(domain_event)

        def clear(self):
            self.events.clear()

    test_event_bus = TestEventBus()

    def test_accept(self):
        event_bus = TestVerificationAcceptor.test_event_bus
        service = PhoneVerificationAcceptor.new(
            TestVerificationAcceptor.test_in_memory_verification_repository,
            event_bus,
        )

        self.assertEqual(len(event_bus.events), 0)

        code = Uuid.new("a8f4f4f8-25e1-4a61-91d4-ec8975a2e580").ok_value
        service.accept(code)

        self.assertEqual(len(event_bus.events), 1)

        event = event_bus.events.pop()

        self.assertEqual(event.name(), Accepted.name())

        event_bus.clear()

    def test_not_accept(self):
        event_bus = TestVerificationAcceptor.test_event_bus
        service = PhoneVerificationAcceptor.new(
            TestVerificationAcceptor.test_in_memory_verification_repository,
            event_bus,
        )

        self.assertEqual(len(event_bus.events), 0)

        code = Uuid.new("00000000-0000-0000-0000-000000000000").ok_value
        service.accept(code)

        self.assertEqual(len(event_bus.events), 1)

        event = event_bus.events.pop()

        self.assertEqual(event.name(), NotAccepted.name())

        event_bus.clear()


if __name__ == '__main__':
    unittest.main()
