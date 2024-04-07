from abc import abstractmethod
from abc import ABCMeta
from typing import Optional

from result import Result

from lib.challenge.email_verification.domain.verification import Verification
from lib.shared.domain.value_object.uuid import Uuid


class Repository(metaclass=ABCMeta):
    """Abstract user repository contract"""

    @abstractmethod
    def save(self, verification: Verification):
        """
        Save a verification in this repository.

        @param verification: verification that wants to save
        @return: Nothing
        """
        pass

    @abstractmethod
    def accept(self, code: Uuid):
        """
        Updates accepted status of verification to true

        :param code:    verification code
        :return: Nothing
        """
        pass
        pass

    @abstractmethod
    def find(self, code: Uuid) -> Result[Optional[Verification], str]:
        """
        Finds a verification with given coder in this repository.
        If any error found, upwards it.

        @param code: code of the verification
        @return: Resulting Verification (None if not found) or error string
        """
        pass
