from __future__ import annotations
from lib.shared.domain.aggregate_root import AggregateRoot
from lib.challenge.user.domain.domain_event.created import Created
from lib.challenge.user.domain.id import Id
from lib.challenge.user.domain.name import Name
from lib.challenge.user.domain.surname import Surname
from lib.challenge.user.domain.email import Email
from lib.challenge.user.domain.phone import Phone
from lib.challenge.user.domain.hobbies import Hobbies


class User(AggregateRoot):
    """"User entity"""

    def __init__(self,
                 id: Id,
                 name: Name,
                 surname: Surname,
                 email: Email,
                 phone: Phone,
                 hobbies: Hobbies,
                 email_verified: bool = False,
                 phone_verified: bool = False,
                 ):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        Initializes aggregate root.

        @param id:      instance of id value object
        @param name:    instance of name value object
        @param surname: instance of surname value object
        @param email:   instance of email value object
        @param phone:   instance of phone value object
        @param hobbies: instance of hobbies value object
        @param email_verified: True if email was verified, False otherwise (default False)
        @param phone_verified: True if phone was verified, False otherwise (default False)
        """

        super().__init__()
        self._id = id
        self._name = name
        self._surname = surname
        self._email = email
        self._phone = phone
        self._hobbies = hobbies
        self._email_verified = email_verified
        self._phone_verified = phone_verified

    @staticmethod
    def new(id: Id,
            name: Name,
            surname: Surname,
            email: Email,
            phone: Phone,
            hobbies: Hobbies,
            email_verified: bool = False,
            phone_verified: bool = False,
            ) -> User:
        """
        Factory method to create a new User object.

        @param id:             instance of id value object
        @param name:           instance of name value object
        @param surname:        instance of surname value object
        @param email:          instance of email value object
        @param phone:          instance of phone value object
        @param hobbies:        instance of hobbies value object
        @param email_verified: True if email was verified, False otherwise (default False)
        @param phone_verified: True if phone was verified, False otherwise (default False)
        @return: Resulting user instance
        """

        user = User(id, name, surname, email, phone, hobbies, email_verified, phone_verified)
        domain_event = Created.new(id.value(),
                                   name.value(),
                                   surname.value(),
                                   email.value(),
                                   phone.value(),
                                   hobbies.value(),
                                   )
        user.record(domain_event)
        return user

    def id(self) -> str:
        """
        Value object primitive accessor.

        Access to the value object is restricted to ensure the Law of Demeter (LoD)

        @return: the string value of user id.
        """

        return self._id.value()

    def name(self) -> str:
        """
        Value object primitive accessor.

        Access to the value object is restricted to ensure the Law of Demeter (LoD)

        @return: the string value of user name.
        """

        return self._name.value()

    def surname(self) -> str:
        """
        Value object primitive accessor.

        Access to the value object is restricted to ensure the Law of Demeter (LoD)

        @return: the string value of user surname.
        """

        return self._surname.value()

    def email(self) -> str:
        """
        Value object primitive accessor.

        Access to the value object is restricted to ensure the Law of Demeter (LoD)

        @return: the string value of user email.
        """

        return self._email.value()

    def phone(self) -> str:
        """
        Value object primitive accessor.

        Access to the value object is restricted to ensure the Law of Demeter (LoD)

        @return: the string value of user phone.
        """

        return self._phone.value()

    def hobbies(self) -> list[str]:
        """
        Value object primitive accessor.

        Access to the value object is restricted to ensure the Law of Demeter (LoD)

        @return: the list of string value of this user hobbies.
        """

        return self._hobbies.value()

    def email_verified(self) -> bool:
        """
        Attribute getter.

        @return: value of private attribute email_verified.
        """

        return self._email_verified

    def phone_verified(self) -> bool:
        """
        Attribute getter.

        @return: value of private attribute phone_verified.
        """

        return self._phone_verified

    def __eq__(self, other):
        """
        Overrides the default behavior of the equality operator to ensure that two users are equal if their values
        contains the same attributes value string.

        @param other: object to compare with
        @return: True if self and other are equals
        """

        if isinstance(other, User):
            return self.id() == other.id() and \
                self.name() == other.name() and \
                self.surname() == other.surname() and \
                self.email() == other.email() and \
                self.phone() == other.phone() and \
                self.hobbies() == other.hobbies() and \
                self.email_verified() == other.email_verified() and \
                self.phone_verified() == other.phone_verified()
        return False

    def __hash__(self):
        """
        Makes User object hashable.
        Because user Id must be unique, it can be used as a hash.

        @return: hash value of User id
        """

        return hash(self._id.value())
