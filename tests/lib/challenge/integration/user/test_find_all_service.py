import unittest

from lib.challenge.user.application.find.all.service import UsersFinder
from lib.challenge.user.domain.user.id import Id
from lib.challenge.user.domain.user.name import Name
from lib.challenge.user.domain.user.surname import Surname
from lib.challenge.user.domain.user.email import Email
from lib.challenge.user.domain.user.phone import Phone
from lib.challenge.user.domain.user.hobbies import Hobbies
from lib.challenge.user.domain.user.user import User
from lib.challenge.user.domain.user.users import Users
from lib.challenge.user.infrastructure.repository.in_memory import InMemory


class TestFindById(unittest.TestCase):
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

    test_user_2 = User.new(
        Id.new("c74e20b5-1d03-424e-9dea-67f88161c294").ok_value,
        Name.new("Mary").ok_value,
        Surname.new("Smith").ok_value,
        Email.new("mary.smith@mail.com").ok_value,
        Phone.new("+34 777 777 777").ok_value,
        Hobbies.new("""
                    Dance
                    Sing
                    """),
    )

    test_in_memory_user_repository = InMemory.new([test_user_1, test_user_2])

    def test_find_all_found(self):
        service = UsersFinder.new(TestFindById.test_in_memory_user_repository)
        users_found = service.find().ok_value
        self.assertEqual(users_found, Users.new([TestFindById.test_user_1, TestFindById.test_user_2]))


if __name__ == '__main__':
    unittest.main()
