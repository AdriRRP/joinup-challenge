from __future__ import annotations
from lib.shared.domain.bus.query.query import Query as AbstractQuery


class Query(AbstractQuery):
    """Query implementation to find user by id"""

    def __init__(self, id: str):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param id: id in string format of user to find
        """
        self._id = id

    @staticmethod
    def new(id: str) -> Query:
        """
        Factory method to create a new Query.

        @param id: id in string format of user to find
        @return: instance of this Query
        """

        query = Query(id)
        return query

    def id(self) -> str:
        """
        Query id primitive accessor.

        @return: the string value of query id.
        """
        return self._id
