from __future__ import annotations

import json
import uuid
from abc import abstractmethod
from abc import ABCMeta
from datetime import datetime


class DomainEvent(metaclass=ABCMeta):

    def __init__(self, aggregate_id: str, event_id: str = None, occurred_on: str = None):
        self._aggregate_id = aggregate_id
        self._event_id = event_id if event_id else str(uuid.uuid4())
        self._occurred_on = occurred_on if occurred_on else datetime.now().isoformat()

    @staticmethod
    @abstractmethod
    def from_primitives(aggregate_id: str, body: dict, event_id: str, occurred_on: str) -> DomainEvent:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
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

    def serialize(self) -> bytes:
        content = {
            'data': {
                'id': self.event_id(),
                'type': self.name(),
                'occurredOn': self.occurred_on(),
                'aggregateId': self.aggregate_id(),
                'attributes': self.to_primitive(),
            },
            'metadata': {}
        }
        return json.dumps(content).encode('utf-8')
