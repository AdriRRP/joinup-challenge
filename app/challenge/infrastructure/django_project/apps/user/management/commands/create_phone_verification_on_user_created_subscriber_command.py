from django.core.management.base import BaseCommand
from app.challenge import kernel


class Command(BaseCommand):
    help = "Run a RabbitMQ subscriber for create_phone_verification_on_user_created"

    def handle(self, *args, **options):
        td = kernel.create_phone_verification_on_user_created_subscriber_th_subscriber
        td.start()
        self.stdout.write("Started `create_phone_verification_on_user_created` Consumer Thread")