from __future__ import annotations
from lib.shared.domain.bus.query.handler import Handler as QueryHandler
from lib.challenge.user.application.find.all.query.query import Query as FindAllQuery
from lib.challenge.user.application.find.all.response.converter import Converter
from lib.challenge.user.application.find.all.response.response import Response as UsersResponse
from lib.challenge.user.application.find.all.service import UsersFinder


class Handler(QueryHandler):
    def __init__(self, users_finder: UsersFinder):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param users_finder: application service to manage queries for find all users
        """

        self._users_finder = users_finder

    @staticmethod
    def new(users_finder: UsersFinder) -> Handler:
        """
        Factory method to create a new Query Handler.

        @param users_finder: application service to manage queries for find all users
        @return: instance of this Query Handler
        """

        query_handler = Handler(users_finder)
        return query_handler

    def handle(self, query: FindAllQuery) -> UsersResponse:
        """
        Executes application service using given query.

        @param query: Query for find all users
        @return: resulting user response
        """

        users_result = self._users_finder.find()
        if users_result.is_err():
            return UsersResponse({'err_msg': users_result.err_value})
        elif len(list(users_result.ok_value)) == 0:
            return UsersResponse.new({})
        else:
            users_result.ok_value.reset_index()
            return Converter.convert(users_result.ok_value)
