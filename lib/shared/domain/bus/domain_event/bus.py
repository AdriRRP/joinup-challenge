from abc import abstractmethod
from abc import ABCMeta

from lib.shared.domain.bus.domain_event.domain_event import DomainEvent


class Bus(metaclass=ABCMeta):
    """Responsible for publishing domain events"""

    @abstractmethod
    def publish(self, domain_event: DomainEvent):
        """
        Publish a domain event

        @param domain_event: instance of DomainEvent contract
        @return: Nothing
        """
        pass
