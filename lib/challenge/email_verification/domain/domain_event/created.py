from __future__ import annotations

from lib.shared.domain.bus.domain_event.domain_event import DomainEvent


class Created(DomainEvent):
    def __init__(self,
                 aggregate_id: str,
                 user_id: str,
                 email: str,
                 event_id: str = None,
                 occurred_on: str = None
                 ):
        super().__init__(aggregate_id, event_id, occurred_on)
        self._user_id = user_id
        self._email = email

    @staticmethod
    def new(aggregate_id: str,
            user_id: str,
            email: str,
            event_id: str = None,
            occurred_on: str = None
            ) -> Created:
        return Created(aggregate_id, user_id, email, event_id, occurred_on)

    @staticmethod
    def from_primitives(aggregate_id: str, body: dict, event_id: str, occurred_on: str) -> DomainEvent:
        created_event = Created(
            aggregate_id,
            body['user_id'],
            body['email'],
            event_id,
            occurred_on)

        return created_event

    @staticmethod
    def event_name(self) -> str:
        return "verification.created"

    def to_primitive(self) -> dict:
        return {
            'code': self._aggregate_id,
            'user_id': self._user_id,
            'email': self._email,
        }
