from __future__ import annotations

from lib.challenge.email_verification.domain.repository import Repository
from lib.challenge.email_verification.domain.verification import Verification
from lib.shared.domain.bus.domain_event.bus import Bus


class VerificationCreator:
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
    def new(repository: Repository, event_bus: Bus) -> VerificationCreator:
        """
        Factory method to create a new UserRegistrar.

        @param repository:    implementation of verification repository
        @param event_bus:     implementation of event bus
        @return: instance of VerificationAcceptor
        """

        service = VerificationCreator(repository, event_bus)
        return service

    def create(self, verification: Verification):
        """
        Create verification provided

        @param verification: code of target verification
        @return: Nothing
        """

        # TODO: Manage errors?

        self._repository.save(verification)
        for event in verification.pull_domain_events():
            self._event_bus.publish(event)
