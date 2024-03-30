from __future__ import annotations
from lib.shared.domain.bus.command.command import Command as AbstractCommand


class Command(AbstractCommand):
    """Command implementation to save a user"""

    def __init__(self,
                 id: str,
                 name: str,
                 surname: str,
                 email: str,
                 phone: str,
                 hobbies: str):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param id:      user id in string format
        @param name:    user name in string format
        @param surname: user surname in string format
        @param email:   user email in string format
        @param phone:   user phone in string format
        @param hobbies: user hobbies in string format
        """

        self._id = id
        self._name = name
        self._surname = surname
        self._email = email
        self._phone = phone
        self._hobbies = hobbies

    @staticmethod
    def new(id: str,
            name: str,
            surname: str,
            email: str,
            phone: str,
            hobbies: str) -> Command:
        """
        Factory method to create a new Command.

        @param id:      user id in string format
        @param name:    user name in string format
        @param surname: user surname in string format
        @param email:   user email in string format
        @param phone:   user phone in string format
        @param hobbies: user hobbies in string format
        @return: instance of this Command
        """

        command = Command(id, name, surname, email, phone, hobbies)
        return command

    def id(self) -> str:
        """
        Command id primitive accessor.

        @return: the string value of command id.
        """
        return self._id

    def name(self) -> str:
        """
        Command name primitive accessor.

        @return: the string value of command name.
        """
        return self._name

    def surname(self) -> str:
        """
        Command surname primitive accessor.

        @return: the string value of command surname.
        """
        return self._surname

    def email(self) -> str:
        """
        Command email primitive accessor.

        @return: the string value of command email.
        """
        return self._email

    def phone(self) -> str:
        """
        Command phone primitive accessor.

        @return: the string value of command phone.
        """
        return self._phone

    def hobbies(self) -> str:
        """
        Command hobbies primitive accessor.

        @return: the string value of command hobbies.
        """
        return self._hobbies
