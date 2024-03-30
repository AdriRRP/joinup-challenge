from lib.challenge.user.application.find.all.response.response import Response as UsersResponse
from lib.challenge.user.domain.users import Users


class Converter:
    """Users entity to UsersResponse converter"""
    @staticmethod
    def convert(users: Users) -> UsersResponse:
        """
        Convert Users entity to a UserResponse.

        @param users: users entity
        @return: resulting user response
        """

        user_list = []
        for user in users:
            user_list.append(
                {
                    'id': user.id(),
                    'name': user.name(),
                    'surname': user.surname(),
                    'email': user.email(),
                    'phone': user.phone(),
                    'hobbies': user.hobbies(),
                    'email_verified': user.email_verified(),
                    'phone_verified': user.phone_verified(),
                }
            )

        response = UsersResponse.new({'users': user_list})

        return response
