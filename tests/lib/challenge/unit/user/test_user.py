import unittest

from lib.challenge.user.domain.user.id import Id
from lib.challenge.user.domain.user.name import Name
from lib.challenge.user.domain.user.surname import Surname
from lib.challenge.user.domain.user.email import Email
from lib.challenge.user.domain.user.phone import Phone
from lib.challenge.user.domain.user.hobbies import Hobbies
from lib.challenge.user.domain.user.user import User


class UserId(unittest.TestCase):
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

        events_again = user.pull_domain_events()

        self.assertEqual(len(events_again), 0)


if __name__ == '__main__':
    unittest.main()
