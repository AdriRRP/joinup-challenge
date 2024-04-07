from django.core.management.base import BaseCommand
from app.challenge import kernel


class Command(BaseCommand):
    help = "Run a RabbitMQ subscriber for accept email verification"

    def handle(self, *args, **options):
        td = kernel.email_verification_acceptor_cmd_subscriber
        td.start()
        self.stdout.write("Started `email_verification_acceptor_cmd_subscriber` Consumer Thread")