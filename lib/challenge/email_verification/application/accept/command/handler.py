from __future__ import annotations
from lib.shared.domain.bus.command.handler import Handler as CommandHandler
from lib.challenge.email_verification.application.accept.command.command import Command as AcceptCommand
from lib.challenge.email_verification.application.accept.service import VerificationAcceptor
from lib.shared.domain.value_object.uuid import Uuid


class Handler(CommandHandler):
    """Command handler implementation to register user"""

    def __init__(self, verification_acceptor: VerificationAcceptor):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param verification_acceptor: application service to manage commands for register users
        """

        self._verification_acceptor = verification_acceptor

    @staticmethod
    def new(verification_acceptor: VerificationAcceptor) -> Handler:
        """
        Factory method to create a new Command Handler.

        @param verification_acceptor: application service to manage commands for register users
        @return: instance of this Command Handler
        """

        command_handler = Handler(verification_acceptor)
        return command_handler

    def handle(self, command: AcceptCommand):
        """
        Executes application service using given command.

        @param command: Command for accept code
        @return: Nothing
        """

        # TODO: Manage errors
        try:
            code = Uuid.new(command.code()).ok_value

            self._verification_acceptor.accept(code)
        except:
            pass
