from abc import abstractmethod
from abc import ABCMeta

from lib.shared.domain.bus.query.query import Query
from lib.shared.domain.bus.query.response import Response


class Bus(metaclass=ABCMeta):
    """Maps a query with a query handler"""

    @abstractmethod
    def ask(self, query: Query) -> Response:
        """
        Looks for a handler for the received query, executes it and returns its response.

        @param query: query instance
        @return: result of executes query's handler
        """
        pass
