from lib.shared.domain.email_service import EmailService


class DummyEmailService(EmailService):
    def send(self, email: str, body: str):
        print(f"to: `{email}`; message: `{body}`")
