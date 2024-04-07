import logging
import smtplib
from email.mime.text import MIMEText

from app.challenge.config import Config
from lib.shared.domain.email_service import EmailService

LOG_FORMAT = 'MAIL: -10s %(message)s'
LOGGER = logging.getLogger(__name__)


class SmtpEmailService(EmailService):

    def __init__(self, config: Config):
        self._subject = "Verify your account"
        self._sender = config.get()['SMTP']['sender']
        self._host = config.get()['SMTP']['host']
        self._port = config.get()['SMTP']['port']

    def send(self, email: str, body: str):
        recipients = [email]
        msg = MIMEText(body)
        msg['Subject'] = self._subject
        msg['From'] = self._sender
        msg['To'] = ', '.join(recipients)
        try:
            smtp = smtplib.SMTP(self._host, self._port)
            smtp.sendmail(self._sender, recipients, msg.as_string())
            LOGGER.info(f"Verification message sent to: `{email}`, body: `{body}`")
        except Exception as e:
            LOGGER.error(f"Error sending mail: {e}")
