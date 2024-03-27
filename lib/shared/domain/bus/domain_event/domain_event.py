from __future__ import annotations
from abc import abstractmethod
from abc import ABCMeta


class DomainEvent(metaclass=ABCMeta):

    def __init__(self, aggregate_id: str, event_id: str, occurred_on: str):
        self._aggregate_id = aggregate_id
        self._event_id = event_id
        self._occurred_on = occurred_on

    @staticmethod
    @abstractmethod
    def from_primitives(aggregate_id: str, body: dict, event_id: str, occurred_on: str) -> DomainEvent:
        pass

    @staticmethod
    @abstractmethod
    def event_name(self) -> str:
        pass

    @abstractmethod
    def to_primitive(self) -> dict:
        pass

    def aggregate_id(self) -> str:
        return self._aggregate_id

    def event_id(self) -> str:
        return self._event_id

    def occurred_on(self) -> str:
        return self._occurred_on
