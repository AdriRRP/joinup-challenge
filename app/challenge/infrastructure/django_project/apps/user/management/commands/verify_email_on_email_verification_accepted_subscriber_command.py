from django.core.management.base import BaseCommand
from app.challenge import kernel


class Command(BaseCommand):
    help = "Run a RabbitMQ subscriber for verify_email_on_email_verification_accepted"

    def handle(self, *args, **options):
        td = kernel.verify_email_on_email_verification_accepted_th_subscriber
        td.start()
        self.stdout.write("Started `verify_email_on_email_verification_accepted` Consumer Thread")