from django.core.management.base import BaseCommand
from app.challenge import kernel


class Command(BaseCommand):
    help = "Run a RabbitMQ subscriber for send_verification_mail_on_email_verification_created"

    def handle(self, *args, **options):
        td = kernel.send_verification_mail_on_email_verification_created_subscriber_th_subscriber
        td.start()
        self.stdout.write("Started `send_verification_mail_on_email_verification_created` Consumer Thread")