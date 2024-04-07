from __future__ import annotations

from lib.challenge.phone_verification.application.create.service import VerificationCreator
from lib.challenge.phone_verification.domain.verification import Verification
from lib.challenge.user.domain.domain_event.created import Created
from lib.challenge.user.domain.phone import Phone
from lib.challenge.user.domain.id import Id
from lib.shared.domain.bus.domain_event.subscriber import Subscriber
from lib.shared.domain.value_object.uuid import Uuid

import uuid


class CreatePhoneVerificationOnUserCreated(Subscriber):
    @staticmethod
    def subscribed_to() -> list[str]:
        return ["challenge.user.created"]

    def __init__(self, verification_creator: VerificationCreator):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param verification_creator: service to execute
        """

        self._verification_creator = verification_creator

    @staticmethod
    def new(verification_creator: VerificationCreator) -> CreatePhoneVerificationOnUserCreated:
        """
        Factory method to create a new CreateVerificationOnUserCreated.

        @param verification_creator: service to execute
        @return: instance of VerificationAcceptor
        """

        subscriber = CreatePhoneVerificationOnUserCreated(verification_creator)
        return subscriber

    def process(self, event: Created):
        """
        Process User Created event

        @param event: user created event
        @return: Nothing
        """

        # TODO: Manage errors

        code = Uuid.new(str(uuid.uuid4())).ok_value
        user_id = Id.new(event.aggregate_id()).ok_value
        phone = Phone.new(event.to_primitive()['phone']).ok_value

        verification = Verification.new(code, user_id, phone)

        self._verification_creator.create(verification)
