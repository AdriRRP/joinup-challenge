from __future__ import annotations

from lib.challenge.phone_verification.domain.domain_event.created import Created
from lib.challenge.user.domain.id import Id
from lib.challenge.user.domain.phone import Phone
from lib.shared.domain.aggregate_root import AggregateRoot
from lib.shared.domain.value_object.uuid import Uuid


class Verification(AggregateRoot):
    """"Verification entity"""

    def __init__(self,
                 code: Uuid,
                 user_id: Id,
                 phone: Phone,
                 accepted: bool = False,
                 ):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        Initializes aggregate root.

        :param code:     Verification code in uuid format
        :param user_id:  Target user id
        :param phone:    Target user phone
        :param accepted: True if verification is accepted, false otherwise (default)
        """

        super().__init__()
        self._code = code
        self._user_id = user_id
        self._phone = phone
        self._accepted = accepted

    @staticmethod
    def new(code: Uuid,
            user_id: Id,
            phone: Phone,
            accepted: bool = False,
            ) -> Verification:
        """
        Factory method to create a new User object.

        :param code:     Verification code in uuid format
        :param user_id:  Target user id
        :param phone:    Target user phone
        :param accepted: True if verification is accepted, false otherwise (default)
        @return: Resulting Verification instance
        """

        verification = Verification(code, user_id, phone, accepted)
        domain_event = Created.new(code.value(),
                                   user_id.value(),
                                   phone.value(),
                                   )
        verification.record(domain_event)
        return verification

    def code(self) -> str:
        """
        Value object primitive accessor.

        Access to the value object is restricted to ensure the Law of Demeter (LoD)

        @return: the string value of verification code
        """

        return self._code.value()

    def user_id(self) -> str:
        """
        Value object primitive accessor.

        Access to the value object is restricted to ensure the Law of Demeter (LoD)

        @return: the string value of user id.
        """

        return self._user_id.value()

    def phone(self) -> str:
        """
        Value object primitive accessor.

        Access to the value object is restricted to ensure the Law of Demeter (LoD)

        @return: the string value of user phone.
        """

        return self._phone.value()

    def accepted(self) -> bool:
        """
        Attribute getter.

        @return: value of private attribute accepted.
        """

        return self._accepted

    def __eq__(self, other):
        """
        Overrides the default behavior of the equality operator to ensure that two verifications are equal if their
        values contains the same attributes value string.

        @param other: object to compare with
        @return: True if self and other are equals
        """

        if isinstance(other, Verification):
            return self.code() == other.code() and \
                self.user_id() == other.user_id() and \
                self.phone() == other.phone() and \
                self.accepted() == other.accepted()
        return False

    def __hash__(self):
        """
        Makes Verification object hashable.
        Because code must be unique, it can be used as a hash.

        @return: hash value of verification code
        """

        return hash(self._code.value())
