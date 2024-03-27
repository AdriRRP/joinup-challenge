from abc import ABCMeta
from abc import abstractmethod

from lib.shared.domain.bus.command.command import Command


class Handler(metaclass=ABCMeta):
    """Assign a domain service to a command"""

    @abstractmethod
    def handle(self, command: Command):
        """
        Calls the domain service in charge of handling the instance of the received command.

        @param command: implementation of a Command contract
        @return: Nothing
        """
        pass
