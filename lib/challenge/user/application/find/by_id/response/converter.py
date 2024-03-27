from lib.challenge.user.application.find.by_id.response.response import Response as UserResponse
from lib.challenge.user.domain.user.user import User


class Converter:
    """User entity to UserResponse converter"""

    @staticmethod
    def convert(user: User) -> UserResponse:
        """
        Convert User entity to a UserResponse.

        @param user: user entity
        @return: resulting user response
        """

        response = UserResponse({
            'id': user.id(),
            'name': user.name(),
            'surname': user.surname(),
            'email': user.email(),
            'phone': user.phone(),
            'hobbies': user.hobbies(),
            'email_verified': user.email_verified(),
            'phone_verified': user.phone_verified(),
        })
        return response
