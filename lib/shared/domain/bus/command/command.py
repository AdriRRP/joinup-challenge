import json
import uuid
from abc import ABCMeta, abstractmethod
from datetime import datetime


class Command(metaclass=ABCMeta):

    def __init__(self, command_id: str = None, occurred_on: str = None):
        self._command_id = command_id if command_id else str(uuid.uuid4())
        self._occurred_on = occurred_on if occurred_on else datetime.now().isoformat()

    @staticmethod
    @abstractmethod
    def command_name() -> str:
        pass

    @abstractmethod
    def to_primitive(self) -> dict:
        pass

    def command_id(self) -> str:
        return self._command_id

    def occurred_on(self) -> str:
        return self._occurred_on

    def serialize(self) -> bytes:
        content = {
            'data': {
                'id': self.command_id(),
                'type': self.command_name(),
                'occurredOn': self.occurred_on(),
                'attributes': self.to_primitive(),
            },
            'metadata': {}
        }
        return json.dumps(content).encode('utf-8')
