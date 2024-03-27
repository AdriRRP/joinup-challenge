import unittest

from lib.challenge.user.application.find.by_id.service import UserFinder
from lib.challenge.user.domain.user.id import Id
from lib.challenge.user.domain.user.name import Name
from lib.challenge.user.domain.user.surname import Surname
from lib.challenge.user.domain.user.email import Email
from lib.challenge.user.domain.user.phone import Phone
from lib.challenge.user.domain.user.hobbies import Hobbies
from lib.challenge.user.domain.user.user import User
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

    test_in_memory_user_repository = InMemory.new([test_user_1])

    def test_find_by_id_found(self):
        service = UserFinder.new(TestFindById.test_in_memory_user_repository)
        id = Id.new("6b0fba2d-e73f-4e33-9e65-92b7621d66b7").ok_value
        user_found = service.find(id).ok_value
        self.assertEqual(user_found, TestFindById.test_user_1)

    def test_find_by_id_not_found(self):
        service = UserFinder.new(TestFindById.test_in_memory_user_repository)
        id = Id.new("00000000-0000-0000-0000-000000000000").ok_value
        user_found = service.find(id).ok_value
        self.assertEqual(user_found, None)


if __name__ == '__main__':
    unittest.main()
