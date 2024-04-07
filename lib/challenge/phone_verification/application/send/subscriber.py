from __future__ import annotations

from lib.challenge.phone_verification.application.send.service import VerificationSender
from lib.challenge.phone_verification.domain.domain_event.created import Created
from lib.challenge.phone_verification.domain.verification import Verification
from lib.challenge.user.domain.phone import Phone
from lib.challenge.user.domain.id import Id
from lib.shared.domain.bus.domain_event.subscriber import Subscriber
from lib.shared.domain.value_object.uuid import Uuid


class SendVerificationSmsOnPhoneVerificationCreated(Subscriber):
    @staticmethod
    def subscribed_to() -> list[str]:
        return ["challenge.phone_verification.created"]

    def __init__(self, verification_sender: VerificationSender):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param verification_sender: service to execute
        """

        self._verification_sender = verification_sender

    @staticmethod
    def new(verification_sender: VerificationSender) -> SendVerificationSmsOnPhoneVerificationCreated:
        """
        Factory method to create a new SendVerificationSmsOnPhoneVerificationCreated.

        @param verification_sender: service to execute
        @return: instance of VerificationSender
        """

        subscriber = SendVerificationSmsOnPhoneVerificationCreated(verification_sender)
        return subscriber

    def process(self, event: Created):
        """
        Process Verification Created event

        @param event: verification created event
        @return: Nothing
        """

        # TODO: Manage errors

        code = Uuid.new(event.aggregate_id()).ok_value
        user_id = Id.new(event.to_primitive()['user_id']).ok_value
        phone = Phone.new(event.to_primitive()['phone']).ok_value

        verification = Verification.new(code, user_id, phone)

        self._verification_sender.send(verification)
