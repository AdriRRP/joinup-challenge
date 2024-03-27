from __future__ import annotations
from lib.shared.domain.bus.query.query import Query as AbstractQuery


class Query(AbstractQuery):
    """Query implementation to find all users"""

    def __init__(self):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.
        """
        pass

    @staticmethod
    def new() -> Query:
        """
        Factory method to create a new Query.

        @return: instance of this Query
        """
        return Query()
