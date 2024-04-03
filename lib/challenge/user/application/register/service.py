from __future__ import annotations

from lib.shared.domain.bus.domain_event.bus import Bus
from lib.challenge.user.domain.repository import Repository
from lib.challenge.user.domain.user import User


class UserRegistrar:
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
    def new(repository: Repository, event_bus: Bus) -> UserRegistrar:
        """
        Factory method to create a new UserRegistrar.

        @param repository: implementation of user repository
        @param event_bus: implementation of event bus
        @return: instance of UserRegistrar
        """

        service = UserRegistrar(repository, event_bus)
        return service

    def register(self, user: User):
        """
        Find user by id in self repository

        @param user: User object to be registered
        @return: Nothing
        """

        # TODO: Manage errors?

        self._repository.save(user)
        for event in user.pull_domain_events():
            self._event_bus.publish(event)
