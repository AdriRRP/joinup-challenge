from abc import ABCMeta
from abc import abstractmethod

from lib.shared.domain.bus.query.query import Query
from lib.shared.domain.bus.query.response import Response


class Handler(metaclass=ABCMeta):
    """Assign a domain service to a query"""

    @abstractmethod
    def handle(self, query: Query) -> Response:
        """
        Calls the domain service in charge of handling the instance of the received query.

        @param query: implementation of a Query contract
        @return: implementation of a Response contract
        """
        pass
