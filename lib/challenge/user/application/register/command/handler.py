from __future__ import annotations
from lib.shared.domain.bus.command.handler import Handler as CommandHandler
from lib.challenge.user.application.register.command.command import Command as RegisterCommand
from lib.challenge.user.application.register.service import UserRegistrar
from lib.challenge.user.domain.email import Email
from lib.challenge.user.domain.hobbies import Hobbies
from lib.challenge.user.domain.id import Id
from lib.challenge.user.domain.name import Name
from lib.challenge.user.domain.phone import Phone
from lib.challenge.user.domain.surname import Surname
from lib.challenge.user.domain.user import User


class Handler(CommandHandler):
    """Command handler implementation to register user"""

    def __init__(self, user_registrar: UserRegistrar):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param user_registrar: application service to manage commands for register users
        """

        self._user_registrar = user_registrar

    @staticmethod
    def new(user_registrar: UserRegistrar) -> Handler:
        """
        Factory method to create a new Command Handler.

        @param user_registrar: application service to manage commands for register users
        @return: instance of this Command Handler
        """

        command_handler = Handler(user_registrar)
        return command_handler

    def handle(self, command: RegisterCommand):
        """
        Executes application service using given command.

        @param command: Command for register user
        @return: Nothing
        """

        # TODO: Manage errors
        try:
            user_id = Id.new(command.id()).ok_value
            user_name = Name.new(command.name()).ok_value
            user_surname = Surname.new(command.surname()).ok_value
            user_email = Email.new(command.email()).ok_value
            user_phone = Phone.new(command.phone()).ok_value
            user_hobbies = Hobbies.new(command.hobbies())

            user = User.new(
                user_id,
                user_name,
                user_surname,
                user_email,
                user_phone,
                user_hobbies,
            )

            self._user_registrar.register(user)
        except:
            pass
