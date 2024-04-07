import logging

from lib.shared.domain.sms_service import SmsService

LOG_FORMAT = 'PHONE: -10s %(message)s'
LOGGER = logging.getLogger(__name__)


class DummySmsService(SmsService):
    def send(self, phone: str, body: str):
        LOGGER.info(f"to: `{phone}`; message: `{body}`")
