import unittest

from lib.shared.domain.bus.domain_event.bus import Bus
from lib.shared.domain.bus.domain_event.domain_event import DomainEvent
from lib.challenge.user.application.find.all.service import UsersFinder
from lib.challenge.user.application.register.service import UserRegistrar
from lib.challenge.user.domain.user.id import Id
from lib.challenge.user.domain.user.name import Name
from lib.challenge.user.domain.user.surname import Surname
from lib.challenge.user.domain.user.email import Email
from lib.challenge.user.domain.user.phone import Phone
from lib.challenge.user.domain.user.hobbies import Hobbies
from lib.challenge.user.domain.user.user import User
from lib.challenge.user.domain.user.users import Users
from lib.challenge.user.infrastructure.repository.in_memory import InMemory


class TestRegister(unittest.TestCase):
    test_user_1 = User.new(
        Id.new("6b0fba2d-e73f-4e33-9e65-92b7621d66b7").ok_value,
        Name.new("John").ok_value,
        Surname.new("Doe").ok_value,
        Email.new("john.doe@mail.com").ok_value,
        Phone.new("+34 666 666 666").ok_value,
        Hobbies.new("""
                    TV Series
                    Music
                    """),
    )

    test_in_memory_user_repository = InMemory.new([])

    class MockEventBus(Bus):
        def __init__(self):
            self.published_events: list[DomainEvent] = []

        def publish(self, domain_event: DomainEvent):
            self.published_events.append(domain_event)

    def test_register(self):
        event_bus = TestRegister.MockEventBus()
        service = UserRegistrar.new(TestRegister.test_in_memory_user_repository, event_bus)
        find_all_service = UsersFinder.new(TestRegister.test_in_memory_user_repository)

        initial_users = find_all_service.find().ok_value
        self.assertEqual(len(initial_users), 0)
        self.assertEqual(len(event_bus.published_events), 0)

        service.register(TestRegister.test_user_1)
        current_users = find_all_service.find().ok_value
        self.assertEqual(current_users, Users.new([TestRegister.test_user_1]))
        self.assertEqual(len(event_bus.published_events), 1)


if __name__ == '__main__':
    unittest.main()
