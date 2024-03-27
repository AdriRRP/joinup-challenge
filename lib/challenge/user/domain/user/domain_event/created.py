from __future__ import annotations
from lib.shared.domain.bus.domain_event.domain_event import DomainEvent


class Created(DomainEvent):
    def __init__(self,
                 aggregate_id: str,
                 name: str,
                 surname: str,
                 email: str,
                 phone: str,
                 hobbies: list[str],
                 event_id: str = None,
                 occurred_on: str = None):
        super().__init__(aggregate_id, event_id, occurred_on)
        self._name = name
        self._surname = surname
        self._email = email
        self._phone = phone
        self._hobbies = hobbies

    @staticmethod
    def new(aggregate_id: str,
            name: str,
            surname: str,
            email: str,
            phone: str,
            hobbies: list[str],
            event_id: str = None,
            occurred_on: str = None) -> Created:
        return Created(aggregate_id, name, surname, email, phone, hobbies, event_id, occurred_on)

    @staticmethod
    def from_primitives(aggregate_id: str, body: dict, event_id: str, occurred_on: str) -> DomainEvent:
        created_event = Created(
            aggregate_id,
            body['name'],
            body['surname'],
            body['email'],
            body['phone'],
            body['hobbies'],
            event_id,
            occurred_on)

        return created_event

    @staticmethod
    def event_name(self) -> str:
        return "user.created"

    def to_primitive(self) -> dict:
        return {
            'name': self._name,
            'surname': self._surname,
            'email': self._email,
            'phone': self._phone,
            'hobbies': self._hobbies,
        }
