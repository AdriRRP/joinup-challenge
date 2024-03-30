from __future__ import annotations

from typing import Optional

from lib.challenge.email_verification.domain.repository import Repository
from lib.challenge.email_verification.domain.verification import Verification
from lib.shared.domain.value_object.uuid import Uuid
from result import Result, Ok, Err


class InMemory(Repository):
    """Implementation for in memory user repository"""
    def __init__(self, verifications: list[Verification] = None):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param verifications: list of verifications preloaded in the repository (empty by default)
        """
        if verifications:
            self._verifications: list[Verification] = verifications
        else:
            self._verifications: list[Verification] = []

    @staticmethod
    def new(verifications: list[Verification] = None) -> InMemory:
        """
        Factory method to create a new user Repository object.

        @param verifications: list of verifications preloaded in the repository (empty by default)
        @return: instance for a new InMemory repository object
        """

        repository = InMemory(verifications)
        return repository

    def accept(self, code: Uuid):
        verification_found =\
            [verification for verification in self._verifications if verification.code() == code.value()]

        if verification_found:
            if len(verification_found) == 1:
                verification_found[0]._accepted = True
            else:
                # send event
                pass
        else:
            # send event
            pass

    def save(self, verification: Verification):
        self._verifications.append(verification)

    def find(self, code: Uuid) -> Result[Optional[Verification], str]:
        verification_found =\
            [verification for verification in self._verifications if verification.code() == code.value()]
        if verification_found:
            if len(verification_found) == 1:
                return Ok(verification_found[0])
            else:
                return Err(f"Found more than verifications with id `{code.value()}`")
        else:
            return Ok(None)

