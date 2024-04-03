from __future__ import annotations

from lib.challenge.email_verification.domain.domain_event.accepted import Accepted
from lib.challenge.user.application.verify_email.service import UserEmailVerifier
from lib.challenge.user.domain.domain_event.created import Created
from lib.challenge.user.domain.id import Id
from lib.shared.domain.bus.domain_event.bus import Bus
from lib.challenge.user.domain.repository import Repository
from lib.shared.domain.bus.domain_event.subscriber import Subscriber


class VerifyEmailOnEmailVerificationAccepted(Subscriber):
    @staticmethod
    def subscribed_to() -> list[str]:
        return [
            "challenge.email_verification.accepted"
        ]

    def __init__(self, user_email_verifier: UserEmailVerifier):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param user_email_verifier: service implementation
        """

        self._verifier = user_email_verifier

    @staticmethod
    def new(user_email_verifier: UserEmailVerifier) -> VerifyEmailOnEmailVerificationAccepted:
        """
        Factory method to create a new UserEmailVerifier.

        @param user_email_verifier: service implementation
        @return: instance of UserEmailVerifier
        """

        subscriber = VerifyEmailOnEmailVerificationAccepted(user_email_verifier)
        return subscriber

    def process(self, event: Accepted):
        """
        Verify user email when email verification accepted event received

        @param event: email verification accepted event
        @return: Nothing
        """

        # TODO: Manage errors?

        id = Id.new(event.to_primitive()['user_id']).ok_value
        self._verifier.verify(id)
