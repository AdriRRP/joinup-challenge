from __future__ import annotations

from typing import Dict, Type

from lib.shared.domain.bus.query.bus import Bus
from lib.shared.domain.bus.query.handler import Handler
from lib.shared.domain.bus.query.query import Query
from lib.shared.domain.bus.query.response import Response


class QueryHandlerNotRegisteredException(Exception):
    """Raised when a given query has not registered handler"""

    def __init__(self, query_type: Type[Query]):
        super().__init__(f"No query handler found for query type `{query_type}`")


class QueryBus(Bus):
    def __init__(self, handlers: Dict[Type[Query], Handler] = None):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param handlers: optional dict that matches a query type with a handler
        """
        if handlers:
            self._handlers: Dict[Type[Query], Handler] = handlers
        else:
            self._handlers: Dict[Type[Query], Handler] = {}

    @staticmethod
    def new(handlers: Dict[Type[Query], Handler] = None) -> QueryBus:
        """
        Factory method to create a new Query bus object.

        @param handlers: handlers: optional dict that matches a query type with a handler
        @return: instance of a query bus
        """

        query_bus = QueryBus(handlers)
        return query_bus

    def ask(self, query: Query) -> Response:
        query_type = type(query)
        if query_type in self._handlers:
            return self._handlers[query_type].handle(query)
        else:
            raise QueryHandlerNotRegisteredException(query_type)

    def register(self, query_type: Type[Query], query_handler: Handler):
        """
        Register a new query type with its corresponding handler.

        @param query_type: query type to register
        @param query_handler: corresponding query handler
        @return: Nothing
        """

        self._handlers[query_type] = query_handler
