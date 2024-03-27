from __future__ import annotations

from typing import Dict, Type

from lib.shared.domain.bus.command.bus import Bus
from lib.shared.domain.bus.command.handler import Handler
from lib.shared.domain.bus.command.command import Command

import threading


class CommandHandlerNotRegisteredException(Exception):
    """Raised when a given command has not registered handler"""

    def __init__(self, command_type: Type[Command]):
        super().__init__(f"No command handler found for query type `{command_type}`")


class CommandBus(Bus):

    def __init__(self, handlers: Dict[Type[Command], Handler] = None):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param handlers: optional dict that matches a query type with a handler
        """

        if handlers:
            self._handlers: Dict[Type[Command], Handler] = handlers
        else:
            self._handlers: Dict[Type[Command], Handler] = {}

    @staticmethod
    def new(handlers: Dict[Type[Command], Handler] = None) -> CommandBus:
        """
        Factory method to create a new Command bus object.

        @param handlers: handlers: optional dict that matches a command type with a handler
        @return: instance of a query bus
        """

        command_bus = CommandBus(handlers)
        return command_bus

    def dispatch(self, command: Command):
        command_type = type(command)
        if command_type in self._handlers:
            thread = threading.Thread(target=self._handlers[command_type].handle(command))
            thread.start()
        else:
            raise CommandHandlerNotRegisteredException(command_type)

    def register(self, command_type: Type[Command], command_handler: Handler):
        """
        Register a new command type with its corresponding handler.

        @param command_type: command type to register
        @param command_handler: corresponding command handler
        @return: Nothing
        """

        self._handlers[command_type] = command_handler
