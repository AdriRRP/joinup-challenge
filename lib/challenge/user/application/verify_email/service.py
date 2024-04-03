from __future__ import annotations

from lib.challenge.user.domain.domain_event.email_verified import EmailVerified
from lib.challenge.user.domain.id import Id
from lib.shared.domain.bus.domain_event.bus import Bus
from lib.challenge.user.domain.repository import Repository


class UserEmailVerifier:
    def __init__(self, repository: Repository, event_bus: Bus):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param repository: implementation of user repository
        @param event_bus: implementation of event bus
        """

        self._repository = repository
        self._event_bus = event_bus

    @staticmethod
    def new(repository: Repository, event_bus: Bus) -> UserEmailVerifier:
        """
        Factory method to create a new UserEmailVerifier.

        @param repository: implementation of user repository
        @param event_bus: implementation of event bus
        @return: instance of UserEmailVerifier
        """

        service = UserEmailVerifier(repository, event_bus)
        return service

    def verify(self, id: Id):
        """
        Verify user with given id

        @param id: User object to be verified
        @return: Nothing
        """

        # TODO: Manage errors?

        found_user = self._repository.find(id).ok_value
        if found_user:
            self._repository.verify_email(id)
            self._event_bus.publish(EmailVerified.new(
                id.value(),
                found_user.name(),
                found_user.surname(),
                found_user.email(),
            ))
