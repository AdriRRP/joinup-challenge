import logging

from lib.shared.domain.email_service import EmailService

LOG_FORMAT = 'MAIL: -10s %(message)s'
LOGGER = logging.getLogger(__name__)


class DummyEmailService(EmailService):
    def send(self, email: str, body: str):
        LOGGER.info(f"to: `{email}`; message: `{body}`")
