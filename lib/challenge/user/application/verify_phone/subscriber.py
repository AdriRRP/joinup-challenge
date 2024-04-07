from __future__ import annotations

from lib.challenge.phone_verification.domain.domain_event.accepted import Accepted
from lib.challenge.user.application.verify_phone.service import UserPhoneVerifier
from lib.challenge.user.domain.id import Id
from lib.shared.domain.bus.domain_event.subscriber import Subscriber


class VerifyPhoneOnPhoneVerificationAccepted(Subscriber):
    @staticmethod
    def subscribed_to() -> list[str]:
        return [
            "challenge.phone_verification.accepted"
        ]

    def __init__(self, user_phone_verifier: UserPhoneVerifier):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param user_phone_verifier: service implementation
        """

        self._verifier = user_phone_verifier

    @staticmethod
    def new(user_phone_verifier: UserPhoneVerifier) -> VerifyPhoneOnPhoneVerificationAccepted:
        """
        Factory method to create a new UserPhoneVerifier.

        @param user_phone_verifier: service implementation
        @return: instance of UserPhoneVerifier
        """

        subscriber = VerifyPhoneOnPhoneVerificationAccepted(user_phone_verifier)
        return subscriber

    def process(self, event: Accepted):
        """
        Verify user phone when phone verification accepted event received

        @param event: phone verification accepted event
        @return: Nothing
        """

        # TODO: Manage errors?

        id = Id.new(event.to_primitive()['user_id']).ok_value
        self._verifier.verify(id)
