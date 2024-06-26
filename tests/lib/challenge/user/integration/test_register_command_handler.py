import unittest

from lib.shared.domain.bus.domain_event.bus import Bus
from lib.shared.domain.bus.domain_event.domain_event import DomainEvent
from lib.challenge.user.application.find.all.service import UsersFinder
from lib.challenge.user.application.register.command.command import Command
from lib.challenge.user.application.register.command.handler import Handler
from lib.challenge.user.application.register.service import UserRegistrar
from lib.challenge.user.domain.id import Id
from lib.challenge.user.domain.name import Name
from lib.challenge.user.domain.surname import Surname
from lib.challenge.user.domain.email import Email
from lib.challenge.user.domain.phone import Phone
from lib.challenge.user.domain.hobbies import Hobbies
from lib.challenge.user.domain.user import User
from lib.challenge.user.domain.users import Users
from lib.challenge.user.infrastructure.repository.in_memory import InMemory


class TestRegisterCommandHandler(unittest.TestCase):
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

    def test_find_by_id_query_handler_found(self):
        event_bus = TestRegisterCommandHandler.MockEventBus()
        service = UserRegistrar.new(TestRegisterCommandHandler.test_in_memory_user_repository, event_bus)
        command_handler = Handler.new(service)
        command = Command.new(
            "6b0fba2d-e73f-4e33-9e65-92b7621d66b7",
            "John",
            "Doe",
            "john.doe@mail.com",
            "+34 666 666 666",
            """
            TV Series
            Music
            """
        )

        find_all_service = UsersFinder.new(TestRegisterCommandHandler.test_in_memory_user_repository)

        initial_users = find_all_service.find().ok_value
        self.assertEqual(len(initial_users), 0)
        self.assertEqual(len(event_bus.published_events), 0)

        service.register(TestRegisterCommandHandler.test_user_1)
        current_users = find_all_service.find().ok_value
        self.assertEqual(current_users, Users.new([TestRegisterCommandHandler.test_user_1]))
        self.assertEqual(len(event_bus.published_events), 1)


if __name__ == '__main__':
    unittest.main()
