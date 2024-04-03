import unittest

from lib.challenge.user.domain.domain_event.created import Created
from lib.challenge.user.domain.id import Id
from lib.challenge.user.domain.name import Name
from lib.challenge.user.domain.surname import Surname
from lib.challenge.user.domain.email import Email
from lib.challenge.user.domain.phone import Phone
from lib.challenge.user.domain.hobbies import Hobbies
from lib.challenge.user.domain.user import User


class UserTest(unittest.TestCase):
    def test_create_user(self):
        id = Id.new("6b0fba2d-e73f-4e33-9e65-92b7621d66b7").ok_value
        name = Name.new("John").ok_value
        surname = Surname.new("Doe").ok_value
        email = Email.new("john.doe@mail.com").ok_value
        phone = Phone.new("+34 666 666 666").ok_value
        hobbies = Hobbies.new("""
        TV Series
        Music
        """)

        user = User.new(id, name, surname, email, phone, hobbies)

        self.assertEqual(user.id(), "6b0fba2d-e73f-4e33-9e65-92b7621d66b7")
        self.assertEqual(user.name(), "John")
        self.assertEqual(user.surname(), "Doe")
        self.assertEqual(user.email(), "john.doe@mail.com")
        self.assertEqual(user.phone(), "+34 666 666 666")
        self.assertEqual(user.hobbies(), ["Music", "TV Series"])

        events = user.pull_domain_events()

        self.assertEqual(len(events), 1)

        event = events[0]

        self.assertTrue(isinstance(event, Created))

        event_primitives = event.to_primitive()
        expected_event_primitives = {
            'name': 'John',
            'surname': 'Doe',
            'email': 'john.doe@mail.com',
            'phone': '+34 666 666 666',
            'hobbies': ['Music', 'TV Series'],
        }

        self.assertEqual(event_primitives, expected_event_primitives)

        events_again = user.pull_domain_events()

        self.assertEqual(len(events_again), 0)


if __name__ == '__main__':
    unittest.main()
