from __future__ import annotations

from lib.challenge.phone_verification.domain.domain_event.sent import Sent
from lib.shared.domain.sms_service import SmsService
from lib.challenge.phone_verification.domain.verification import Verification
from lib.shared.domain.bus.domain_event.bus import Bus


class VerificationSender:
    def __init__(self, sms_service: SmsService, event_bus: Bus, verification_route: str):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param sms_service:        implementation of sms service
        @param event_bus:          implementation of event bus
        @param verification_route: endpoint to accept verification
        """

        self._sms_service = sms_service
        self._event_bus = event_bus
        self._verification_route = verification_route

    @staticmethod
    def new(sms_service: SmsService, event_bus: Bus, verification_route: str) -> VerificationSender:
        """
        Factory method to create a new VerificationSender.

        @param sms_service:      implementation of sms service
        @param event_bus:          implementation of event bus
        @param verification_route: endpoint to accept verification
        @return: instance of VerificationAcceptor
        """

        service = VerificationSender(sms_service, event_bus, verification_route)
        return service

    def send(self, verification: Verification):
        """
        Send verification sms

        @param verification: verification instance
        @return: Nothing
        """

        # TODO: Compose verification link dynamically

        sms_body = f"Click {self._verification_route}/{verification.code()} to verify your phone"

        self._sms_service.send(verification.phone(), sms_body)
        self._event_bus.publish(Sent.new(
            verification.code(),
            verification.user_id(),
            verification.phone(),
        ))
