from app.challenge.infrastructure.bus.command.rabbitmq_command_bus import RabbitMQCommandBus
from app.challenge.infrastructure.bus.domain_event.rabbitmq_event_bus_sync import RabbitMQEventBus
from app.challenge.infrastructure.subscribers.command.user.rabbitmq_creator import RabbitUserCreator
from app.challenge.infrastructure.subscribers.command.email_verification.rabbitmq_acceptor import \
    RabbitEmailVerificationAcceptor
from app.challenge.infrastructure.subscribers.event.email_verification.rabbitmq_create_email_verification_on_user_created import \
    RabbitMQCreateEmailVerificationOnUserCreatedSubscriber
from app.challenge.infrastructure.subscribers.event.email_verification.rabbitmq_send_verification_mail_on_email_verification_created import \
    RabbitMQSendVerificationMailOnEmailVerificationCreatedSubscriber
from app.challenge.infrastructure.subscribers.event.user.rabbitmq_verify_email_on_email_verification_accepted import \
    RabbitMQVerifyEmailOnEmailVerificationAcceptedSubscriber
from app.challenge.infrastructure.external_services.dummy_email_service import DummyEmailService
from lib.challenge.email_verification.application.accept.command.command import Command as AcceptEmailVerificationCommand
from lib.challenge.email_verification.application.accept.command.handler import Handler as AcceptEmailVerificationCommandHandler
from lib.challenge.email_verification.application.accept.service import EmailVerificationAcceptor
from lib.challenge.email_verification.application.create.service import VerificationCreator
from lib.challenge.email_verification.application.create.subscriber import CreateEmailVerificationOnUserCreated
from lib.challenge.email_verification.application.send.service import VerificationSender
from lib.challenge.email_verification.application.send.subscriber import SendVerificationMailOnEmailVerificationCreated
from lib.challenge.user.application.verify_email.service import UserEmailVerifier
from lib.challenge.user.application.verify_email.subscriber import VerifyEmailOnEmailVerificationAccepted
from lib.shared.infrastructure.bus.command_bus import CommandBus
from lib.shared.infrastructure.bus.query_bus import QueryBus

from lib.challenge.user.application.find.all.query.handler import Handler as AllUsersQueryHandler
from lib.challenge.user.application.find.all.query.query import Query as AllUsersQuery
from lib.challenge.user.application.find.all.service import UsersFinder
from lib.challenge.user.application.find.by_id.query.handler import Handler as ByIdUserQueryHandler
from lib.challenge.user.application.find.by_id.query.query import Query as ByIdUserQuery
from lib.challenge.user.application.find.by_id.service import UserFinder
from lib.challenge.user.application.register.command.handler import Handler as UserRegistrarCommandHandler
from lib.challenge.user.application.register.command.command import Command as UserRegistrarCommand
from lib.challenge.user.application.register.service import UserRegistrar

from app.challenge.config import Config
from app.challenge.infrastructure.repository.user.mongo import Mongo as MongoUserRepository
from app.challenge.infrastructure.repository.email_verification.mongo import Mongo as MongoEmailVerificationRepository

# App configuration
config = Config.new()

# Repositories
user_repository = MongoUserRepository.new(config)
email_verification_repository = MongoEmailVerificationRepository.new(config)

# query services
user_by_id_finder = UserFinder.new(user_repository)
all_users_finder = UsersFinder.new(user_repository)

# query handlers
user_by_id_query_handler = ByIdUserQueryHandler.new(user_by_id_finder)
all_users_query_handler = AllUsersQueryHandler.new(all_users_finder)

# query bus
query_bus = QueryBus.new()
query_bus.register(ByIdUserQuery, user_by_id_query_handler)
query_bus.register(AllUsersQuery, all_users_query_handler)

# event bus
event_bus = RabbitMQEventBus.new(config)

# email service
email_service = DummyEmailService()

# event services
user_email_verifier_service = UserEmailVerifier.new(user_repository, event_bus)
verification_creator_service = VerificationCreator(email_verification_repository, event_bus)
verification_sender_service = VerificationSender(
    email_service,
    event_bus,
    "http://127.0.0.1:8000/api/v1/verification"
)

# event subscribers
verify_email_on_email_verification_accepted =\
    VerifyEmailOnEmailVerificationAccepted(user_email_verifier_service)
create_email_verification_on_user_created_subscriber =\
    CreateEmailVerificationOnUserCreated(verification_creator_service)
send_verification_mail_on_email_verification_created_subscriber =\
    SendVerificationMailOnEmailVerificationCreated(verification_sender_service)

# event subscribers threads
verify_email_on_email_verification_accepted_th_subscriber =\
    RabbitMQVerifyEmailOnEmailVerificationAcceptedSubscriber(
        config,
        verify_email_on_email_verification_accepted
    )
create_email_verification_on_user_created_subscriber_th_subscriber =\
    RabbitMQCreateEmailVerificationOnUserCreatedSubscriber(
        config,
        create_email_verification_on_user_created_subscriber
    )
send_verification_mail_on_email_verification_created_subscriber_th_subscriber =\
    RabbitMQSendVerificationMailOnEmailVerificationCreatedSubscriber(
        config,
        send_verification_mail_on_email_verification_created_subscriber
    )
# command services
user_registrar = UserRegistrar.new(user_repository, event_bus)
verification_acceptor = EmailVerificationAcceptor.new(email_verification_repository, event_bus)

# command handlers
register_user_command_handler = UserRegistrarCommandHandler.new(user_registrar)
accept_verification_command_handler = AcceptEmailVerificationCommandHandler.new(verification_acceptor)

# command subscribers
user_creator_cmd_subscriber = RabbitUserCreator(config, register_user_command_handler)
email_verification_acceptor_cmd_subscriber = RabbitEmailVerificationAcceptor(config, accept_verification_command_handler)

# command bus
command_bus = RabbitMQCommandBus.new(config)
