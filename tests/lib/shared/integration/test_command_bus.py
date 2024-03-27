from __future__ import annotations

import time
import unittest
from typing import Dict

from lib.shared.domain.bus.command.handler import Handler
from lib.shared.domain.bus.command.command import Command
from lib.shared.infrastructure.bus.command_bus import CommandBus, CommandHandlerNotRegisteredException


class TestSingleton:
    counters: Dict[str, int] = {}


class ConcreteCommand(Command):
    def __init__(self, f_name: str):
        self.f_name = f_name


class ConcreteCommandHandler(Handler):
    def handle(self, command: ConcreteCommand):
        TestSingleton.counters[command.f_name] += 1
        print("Thread end!")


class TestCommandBus(unittest.TestCase):

    def test_create_command_bus_with_handlers_ok(self):
        f_name = "test_create_command_bus_with_handlers_ok"
        concrete_command = ConcreteCommand(f_name)
        concrete_command_handler = ConcreteCommandHandler()
        handlers = {ConcreteCommand: concrete_command_handler}
        command_bus = CommandBus.new(handlers)

        TestSingleton.counters[f_name] = 0

        command_bus.dispatch(concrete_command)

        # print message will be written
        time.sleep(0.5)

        self.assertTrue(TestSingleton.counters[f_name] == 1)

    def test_empty_command_bus_add_handler_ok(self):
        f_name = "test_empty_command_bus_add_handler_ok"
        concrete_command = ConcreteCommand(f_name)
        concrete_command_handler = ConcreteCommandHandler()
        command_bus = CommandBus.new()

        command_bus.register(ConcreteCommand, concrete_command_handler)

        TestSingleton.counters[f_name] = 0

        command_bus.dispatch(concrete_command)

        # print message will be written
        time.sleep(0.5)

        self.assertTrue(TestSingleton.counters[f_name] == 1)

    def test_throws_exception_when_no_handler_ok(self):
        f_name = "test_throws_exception_when_no_handler_ok"
        concrete_command = ConcreteCommand(f_name)
        command_bus = CommandBus.new()

        with self.assertRaises(CommandHandlerNotRegisteredException):
            command_bus.dispatch(concrete_command)
