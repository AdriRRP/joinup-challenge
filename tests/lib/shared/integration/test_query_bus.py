from __future__ import annotations
import unittest

from lib.shared.domain.bus.query.handler import Handler
from lib.shared.domain.bus.query.query import Query
from lib.shared.domain.bus.query.response import Response
from lib.shared.infrastructure.bus.query_bus import QueryBus, QueryHandlerNotRegisteredException


class ConcreteQuery(Query):
    pass


class ConcreteResponse(Response):
    def __init__(self):
        self.ok = True


class ConcreteQueryHandler(Handler):
    def handle(self, query: ConcreteQuery) -> ConcreteResponse:
        return ConcreteResponse()


class TestQueryBus(unittest.TestCase):

    def test_create_query_bus_with_handlers_ok(self):
        concrete_query = ConcreteQuery()
        concrete_query_handler = ConcreteQueryHandler()
        handlers = {ConcreteQuery: concrete_query_handler}
        query_bus = QueryBus.new(handlers)

        response = query_bus.ask(concrete_query)

        self.assertTrue(hasattr(response, 'ok'))

    def test_empty_query_bus_add_handler_ok(self):
        concrete_query = ConcreteQuery()
        concrete_query_handler = ConcreteQueryHandler()
        query_bus = QueryBus.new()

        query_bus.register(ConcreteQuery, concrete_query_handler)

        response = query_bus.ask(concrete_query)

        self.assertTrue(hasattr(response, 'ok'))

    def test_throws_exception_when_no_handler_ok(self):
        concrete_query = ConcreteQuery()
        query_bus = QueryBus.new()

        with self.assertRaises(QueryHandlerNotRegisteredException):
            query_bus.ask(concrete_query)

