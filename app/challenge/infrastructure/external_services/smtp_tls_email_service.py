import logging
import smtplib
from email.mime.text import MIMEText

from app.challenge.config import Config
from lib.shared.domain.email_service import EmailService

LOG_FORMAT = 'MAIL: -10s %(message)s'
LOGGER = logging.getLogger(__name__)


class SmtpTlsEmailService(EmailService):

    def __init__(self, config: Config):
        self._subject = "Verify your account"
        self._sender = config.get()['SMTP']['sender']
        self._password = config.get()['SMTP']['password']
        self._host = config.get()['SMTP']['host']
        self._port = config.get()['SMTP']['port']

    def send(self, email: str, body: str):
        recipients = [email]
        msg = MIMEText(body)
        msg['Subject'] = self._subject
        msg['From'] = self._sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL(self._host, self._port) as smtp_server:
            smtp_server.login(self._sender, self._password)
            smtp_server.sendmail(self._sender, recipients, msg.as_string())
        print("")
        LOGGER.info(f"Verification message sent to: `{email}`, body: `{body}`")
