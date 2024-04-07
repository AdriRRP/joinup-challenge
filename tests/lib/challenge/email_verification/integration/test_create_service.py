import unittest

from lib.challenge.phone_verification.application.create.service import VerificationCreator
from lib.challenge.phone_verification.domain.domain_event.created import Created
from lib.challenge.phone_verification.domain.verification import Verification
from lib.challenge.phone_verification.infrastructure.repository.in_memory import InMemory
from lib.challenge.user.domain.phone import Phone
from lib.challenge.user.domain.id import Id
from lib.shared.domain.bus.domain_event.domain_event import DomainEvent
from lib.shared.domain.value_object.uuid import Uuid
from lib.shared.domain.bus.domain_event.bus import Bus as EventBus


class TestVerificationCreator(unittest.TestCase):
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

    def test_create(self):
        event_bus = TestVerificationCreator.test_event_bus
        verification = TestVerificationCreator.test_verification
        repository = TestVerificationCreator.test_in_memory_verification_repository
        service = VerificationCreator.new(
            repository,
            event_bus,
        )

        self.assertEqual(len(event_bus.events), 0)

        service.create(verification)

        self.assertEqual(len(event_bus.events), 1)

        event = event_bus.events.pop()

        self.assertEqual(type(event).__name__, Created.__name__)

        event_bus.clear()

        repo_verifications = repository._verifications

        self.assertEqual(len(repo_verifications), 1)
        self.assertEqual(repo_verifications[0], verification)


if __name__ == '__main__':
    unittest.main()
