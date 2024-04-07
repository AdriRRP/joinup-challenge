from __future__ import annotations

from lib.shared.domain.bus.domain_event.domain_event import DomainEvent


class Accepted(DomainEvent):
    def __init__(self,
                 aggregate_id: str,
                 user_id: str,
                 phone: str,
                 event_id: str = None,
                 occurred_on: str = None
                 ):
        super().__init__(aggregate_id, event_id, occurred_on)
        self._user_id = user_id
        self._phone = phone

    @staticmethod
    def new(aggregate_id: str,
            user_id: str,
            phone: str,
            event_id: str = None,
            occurred_on: str = None
            ) -> Accepted:
        return Accepted(aggregate_id, user_id, phone, event_id, occurred_on)

    @staticmethod
    def from_primitives(aggregate_id: str, body: dict, event_id: str, occurred_on: str) -> DomainEvent:
        created_event = Accepted(
            aggregate_id,
            body['user_id'],
            body['phone'],
            event_id,
            occurred_on)

        return created_event

    @staticmethod
    def name() -> str:
        return "challenge.phone_verification.accepted"

    def to_primitive(self) -> dict:
        return {
            'user_id': self._user_id,
            'phone': self._phone,
        }
