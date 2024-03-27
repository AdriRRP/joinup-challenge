from abc import abstractmethod
from abc import ABCMeta

from lib.shared.domain.bus.command.command import Command


class Bus(metaclass=ABCMeta):
    """Maps a command with a command handler"""

    @abstractmethod
    def dispatch(self, command: Command):
        """
        Looks for a handler for the received command and executes it.

        @param command: Command contract instance
        @return: Nothing
        """
        pass
