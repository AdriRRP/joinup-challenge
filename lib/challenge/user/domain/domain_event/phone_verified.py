from __future__ import annotations
from lib.shared.domain.bus.domain_event.domain_event import DomainEvent


class PhoneVerified(DomainEvent):
    def __init__(self,
                 aggregate_id: str,
                 name: str,
                 surname: str,
                 phone: str,
                 event_id: str = None,
                 occurred_on: str = None):
        super().__init__(aggregate_id, event_id, occurred_on)
        self._name = name
        self._surname = surname
        self._phone = phone

    @staticmethod
    def new(aggregate_id: str,
            name: str,
            surname: str,
            phone: str,
            event_id: str = None,
            occurred_on: str = None) -> PhoneVerified:
        return PhoneVerified(aggregate_id, name, surname, phone, event_id, occurred_on)

    @staticmethod
    def from_primitives(aggregate_id: str, body: dict, event_id: str, occurred_on: str) -> DomainEvent:
        created_event = PhoneVerified(
            aggregate_id,
            body['name'],
            body['surname'],
            body['phone'],
            event_id,
            occurred_on)

        return created_event

    @staticmethod
    def name() -> str:
        return "challenge.user.phone_verified"

    def to_primitive(self) -> dict:
        return {
            'name': self._name,
            'surname': self._surname,
            'phone': self._phone,
        }
