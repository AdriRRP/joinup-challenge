from __future__ import annotations
from lib.shared.domain.bus.query.handler import Handler as QueryHandler
from lib.challenge.user.application.find.by_id.query.query import Query as FindByIdQuery
from lib.challenge.user.application.find.by_id.response.converter import Converter
from lib.challenge.user.application.find.by_id.response.response import Response as UserResponse
from lib.challenge.user.application.find.by_id.service import UserFinder
from lib.challenge.user.domain.id import Id


class Handler(QueryHandler):
    """Query handler implementation to find user by id"""

    def __init__(self, user_finder: UserFinder):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param user_finder: application service to manage queries for find user by id
        """

        self._user_finder = user_finder

    @staticmethod
    def new(user_finder: UserFinder) -> Handler:
        """
        Factory method to create a new Query Handler.

        @param user_finder: application service to manage queries for find user by id
        @return: instance of this Query Handler
        """

        query_handler = Handler(user_finder)
        return query_handler

    def handle(self, query: FindByIdQuery) -> UserResponse:
        """
        Executes application service using given query.

        @param query: Query for find user by id
        @return: resulting user response
        """
        user_id = Id.new(query.id())

        if user_id.is_ok():
            user_result = self._user_finder.find(user_id.ok_value)
            if user_result.is_err():
                return UserResponse.new({'err_msg': user_result.err_value})
            elif user_result.ok_value is None:
                return UserResponse.new({})
            else:
                return Converter.convert(user_result.ok_value)
        else:
            return UserResponse.new({'err_msg': user_id.err_value})

