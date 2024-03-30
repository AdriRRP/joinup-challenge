from __future__ import annotations

from lib.challenge.email_verification.domain.domain_event.sent import Sent
from lib.shared.domain.email_service import EmailService
from lib.challenge.email_verification.domain.verification import Verification
from lib.shared.domain.bus.domain_event.bus import Bus


class VerificationSender:
    def __init__(self, email_service: EmailService, event_bus: Bus, verification_route: str):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param email_service:      implementation of email service
        @param event_bus:          implementation of event bus
        @param verification_route: endpoint to accept verification
        """

        self._email_service = email_service
        self._event_bus = event_bus
        self._verification_route = verification_route

    @staticmethod
    def new(email_service: EmailService, event_bus: Bus, verification_route: str) -> VerificationSender:
        """
        Factory method to create a new VerificationSender.

        @param email_service:      implementation of email service
        @param event_bus:          implementation of event bus
        @param verification_route: endpoint to accept verification
        @return: instance of VerificationAcceptor
        """

        service = VerificationSender(email_service, event_bus, verification_route)
        return service

    def send(self, verification: Verification):
        """
        Send verification mail

        @param verification: verification instance
        @return: Nothing
        """

        # TODO: Compose verification link dynamically

        email_body = f"Click {self._verification_route}/{verification.code()} to verify your email"

        self._email_service.send(verification.email(), email_body)
        self._event_bus.publish(Sent.new(
            verification.code(),
            verification.user_id(),
            verification.email(),
        ))
