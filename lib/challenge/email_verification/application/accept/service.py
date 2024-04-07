from __future__ import annotations

from lib.challenge.email_verification.domain.domain_event.accepted import Accepted
from lib.challenge.email_verification.domain.domain_event.not_accepted import NotAccepted
from lib.challenge.email_verification.domain.repository import Repository
from lib.shared.domain.bus.domain_event.bus import Bus
from lib.shared.domain.value_object.uuid import Uuid


class EmailVerificationAcceptor:
    def __init__(self, repository: Repository, event_bus: Bus):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param repository:    implementation of verification repository
        @param event_bus:     implementation of event bus
        """

        self._repository = repository
        self._event_bus = event_bus

    @staticmethod
    def new(repository: Repository, event_bus: Bus) -> EmailVerificationAcceptor:
        """
        Factory method to create a new UserRegistrar.

        @param repository:    implementation of verification repository
        @param event_bus:     implementation of event bus
        @return: instance of VerificationAcceptor
        """

        service = EmailVerificationAcceptor(repository, event_bus)
        return service

    def accept(self, code: Uuid):
        """
        Accept verification with code provided

        @param code: code of target verification
        @return: Nothing
        """

        verification_result = self._repository.find(code)

        if verification_result.is_ok() and verification_result.ok_value:
            print("verification OK")
            verification = verification_result.ok_value
            self._repository.accept(code)
            self._event_bus.publish(
                Accepted.new(
                    verification.code(),
                    verification.user_id(),
                    verification.email(),
                ),
            )
        else:
            print("verification KO")
            self._event_bus.publish(
                NotAccepted.new(
                    code.value(),
                    f"Verification with code `{code.value()}` not found",
                ),
            )
