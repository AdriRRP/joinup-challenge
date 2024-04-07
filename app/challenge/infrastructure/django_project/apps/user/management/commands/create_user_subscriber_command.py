from django.core.management.base import BaseCommand
from app.challenge import kernel


class Command(BaseCommand):
    help = "Run a RabbitMQ subscriber for create user"

    def handle(self, *args, **options):
        td = kernel.user_creator_cmd_subscriber
        td.start()
        self.stdout.write("Started `user_creator_cmd_subscriber` Consumer Thread")