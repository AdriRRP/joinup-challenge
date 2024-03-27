from lib.shared.infrastructure.bus.command_bus import CommandBus
from lib.shared.domain.bus.domain_event.bus import Bus
from lib.shared.domain.bus.domain_event.domain_event import DomainEvent
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
from app.challenge.infrastructure.repository.mongo import Mongo

# App configuration
config = Config.new()

# Repository
user_repository = Mongo.new(config)

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
class DummyEventBus(Bus):
    def __init__(self):
        pass

    def publish(self, domain_event: DomainEvent):
        print(domain_event)


event_bus = DummyEventBus()

# command services
user_registrar = UserRegistrar.new(user_repository, event_bus)

# command handlers
register_user_command_handler = UserRegistrarCommandHandler.new(user_registrar)

# command bus
command_bus = CommandBus.new()
command_bus.register(UserRegistrarCommand, register_user_command_handler)