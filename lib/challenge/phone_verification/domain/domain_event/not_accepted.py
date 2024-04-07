from __future__ import annotations

from lib.shared.domain.bus.domain_event.domain_event import DomainEvent


class NotAccepted(DomainEvent):
    def __init__(self,
                 aggregate_id: str,
                 cause: str,
                 event_id: str = None,
                 occurred_on: str = None
                 ):
        super().__init__(aggregate_id, event_id, occurred_on)
        self._cause = cause

    @staticmethod
    def new(aggregate_id: str,
            cause: str,
            event_id: str = None,
            occurred_on: str = None
            ) -> NotAccepted:
        return NotAccepted(aggregate_id, cause, event_id, occurred_on)

    @staticmethod
    def from_primitives(aggregate_id: str, body: dict, event_id: str, occurred_on: str) -> DomainEvent:
        created_event = NotAccepted(
            aggregate_id,
            body['cause'],
            event_id,
            occurred_on)

        return created_event

    @staticmethod
    def name() -> str:
        return "challenge.phone_verification.not_accepted"

    def to_primitive(self) -> dict:
        return {
            'cause': self._cause,
        }
