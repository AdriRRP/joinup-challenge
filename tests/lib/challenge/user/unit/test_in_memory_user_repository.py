import unittest

from lib.challenge.user.domain.id import Id
from lib.challenge.user.domain.name import Name
from lib.challenge.user.domain.surname import Surname
from lib.challenge.user.domain.email import Email
from lib.challenge.user.domain.phone import Phone
from lib.challenge.user.domain.hobbies import Hobbies
from lib.challenge.user.domain.user import User
from lib.challenge.user.domain.users import Users
from lib.challenge.user.infrastructure.repository.in_memory import InMemory


class TestInMemoryUserRepository(unittest.TestCase):
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

    test_user_3 = User.new(
        Id.new("f67ef401-716b-4846-bc74-f10e3290e343").ok_value,
        Name.new("Unknown").ok_value,
        Surname.new("Void").ok_value,
        Email.new("unknown.void@mail.com").ok_value,
        Phone.new("+34 000 000 000").ok_value,
        Hobbies.new(),
    )

    test_users = [test_user_1, test_user_2]

    def test_create_in_memory_user_repository(self):
        repository = InMemory.new(TestInMemoryUserRepository.test_users)
        repository_content = repository.find_all().ok_value
        self.assertEqual(len(repository_content), 2)

    def test_in_memory_user_repository_found_by_id(self):
        repository = InMemory.new(TestInMemoryUserRepository.test_users)
        id = Id.new("6b0fba2d-e73f-4e33-9e65-92b7621d66b7").ok_value
        user_found = repository.find(id).ok_value
        self.assertEqual(user_found, TestInMemoryUserRepository.test_user_1)

    def test_in_memory_user_repository_not_found_by_id(self):
        repository = InMemory.new(TestInMemoryUserRepository.test_users)
        id = Id.new("00000000-0000-0000-0000-000000000000").ok_value
        user_found = repository.find(id).ok_value
        self.assertEqual(user_found, None)

    def test_in_memory_user_repository_found_all(self):
        repository = InMemory.new(TestInMemoryUserRepository.test_users)
        users_found = repository.find_all().ok_value
        expected_users = Users.new(TestInMemoryUserRepository.test_users)
        self.assertEqual(users_found, expected_users)

    def test_in_memory_user_repository_save(self):
        repository = InMemory.new(TestInMemoryUserRepository.test_users)
        repository.save(TestInMemoryUserRepository.test_user_3)
        users_found = repository.find_all().ok_value
        self.assertEqual(len(users_found), 3)

    def test_in_memory_user_repository_verify_email(self):
        repository = InMemory.new(TestInMemoryUserRepository.test_users)
        user_1 = TestInMemoryUserRepository.test_user_1
        id_user_1 = Id.new(user_1.id()).ok_value
        found_user_1 = repository.find(id_user_1).ok_value
        self.assertFalse(found_user_1.email_verified())
        repository.verify_email(id_user_1)
        found_user_1 = repository.find(id_user_1).ok_value
        self.assertTrue(found_user_1.email_verified())

    def test_in_memory_user_repository_verify_phone(self):
        repository = InMemory.new(TestInMemoryUserRepository.test_users)
        user_1 = TestInMemoryUserRepository.test_user_1
        id_user_1 = Id.new(user_1.id()).ok_value
        found_user_1 = repository.find(id_user_1).ok_value
        self.assertFalse(found_user_1.phone_verified())
        repository.verify_phone(id_user_1)
        found_user_1 = repository.find(id_user_1).ok_value
        self.assertTrue(found_user_1.phone_verified())


if __name__ == '__main__':
    unittest.main()
