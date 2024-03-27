from typing import Optional

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from lib.challenge.user.application.find.all.query.query import Query as AllUsersQuery
from lib.challenge.user.application.find.by_id.query.query import Query as ByIdUserQuery
from lib.challenge.user.application.register.command.command import Command as RegisterCommand
from app.challenge import kernel


class AllUsersAPIView(APIView):
    """Manages all users data retrieve"""

    def get(self, request, version):
        if version == 'v1':
            query = AllUsersQuery.new()
            users_response = kernel.query_bus.ask(query)

            if users_response.is_error():
                return Response(
                    data={'err_msg': users_response.get_error_message()},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif users_response.is_empty():
                return Response(
                    data={},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    data=users_response.get_users(),
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                data={'err_msg': f"Version {request.version} not yet supported"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ByIdUserAPIView(APIView):
    """Manages user by id data retrieve"""

    def get(self, request, version, id):
        if version == 'v1':
            query = ByIdUserQuery.new(id)
            user_response = kernel.query_bus.ask(query)

            if user_response.is_error():
                return Response(
                    data={'err_msg': user_response.get_error_message()},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif user_response.is_empty():
                return Response(
                    data={},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    data=user_response.get_user(),
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                data={'err_msg': f"Version {request.version} not yet supported"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RegisterUserAPIView(APIView):
    """Manages register users"""

    def put(self, request, version):
        if version == 'v1':
            for field in ['id', 'name', 'surname', 'email', 'phone', 'hobbies']:
                opt_response = contains_field_precondition(field, request.data)
                if opt_response:
                    return opt_response
            command = RegisterCommand.new(
                request.data['id'],
                request.data['name'],
                request.data['surname'],
                request.data['email'],
                request.data['phone'],
                request.data['hobbies'],
            )
            kernel.command_bus.dispatch(command)
            return Response(
                data={'status': f"Request accepted, you will be notified when finished"},
                status=status.HTTP_202_ACCEPTED
            )
        else:
            return Response(
                data={'err_msg': f"Version {request.version} not yet supported"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def contains_field_precondition(field_name: str, request) -> Optional[Response]:
    if field_name not in request:
        return Response(
            data={'err_msg': f"Required field '{field_name}' not found in request"},
            status=status.HTTP_412_PRECONDITION_FAILED
        )
    else:
        return None
