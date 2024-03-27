import unittest

from lib.challenge.user.application.find.all.query.handler import Handler
from lib.challenge.user.application.find.all.service import UsersFinder
from lib.challenge.user.application.find.all.query.query import Query
from lib.challenge.user.application.find.all.response.response import Response
from lib.challenge.user.domain.user.id import Id
from lib.challenge.user.domain.user.name import Name
from lib.challenge.user.domain.user.surname import Surname
from lib.challenge.user.domain.user.email import Email
from lib.challenge.user.domain.user.phone import Phone
from lib.challenge.user.domain.user.hobbies import Hobbies
from lib.challenge.user.domain.user.user import User
from lib.challenge.user.infrastructure.repository.in_memory import InMemory


class TestFindAllQueryHandler(unittest.TestCase):
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

    test_in_memory_user_empty_repository = InMemory.new([])
    test_in_memory_user_repository = InMemory.new([test_user_1])

    def test_find_all_query_handler_found(self):
        service = UsersFinder.new(TestFindAllQueryHandler.test_in_memory_user_repository)
        query_handler = Handler.new(service)
        query = Query.new()

        response = query_handler.handle(query)

        expected_response = Response.new({
            'users': [
                {
                    'id': "6b0fba2d-e73f-4e33-9e65-92b7621d66b7",
                    'name': "John",
                    'surname': "Doe",
                    'email': "john.doe@mail.com",
                    'phone': "+34 666 666 666",
                    'hobbies': ["Music", "TV Series"],
                    'email_verified': False,
                    'phone_verified': False,
                }
            ]
        })

        self.assertTrue(not response.is_empty())
        self.assertTrue(not response.is_error())
        self.assertEqual(response, expected_response)

    def test_find_all_query_handler_empty(self):
        service = UsersFinder.new(TestFindAllQueryHandler.test_in_memory_user_empty_repository)
        query_handler = Handler.new(service)
        query = Query.new()

        response = query_handler.handle(query)

        expected_response = Response.new({})

        self.assertTrue(response.is_empty())
        self.assertTrue(not response.is_error())
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
