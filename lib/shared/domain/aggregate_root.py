from abc import ABCMeta


class AggregateRoot(metaclass=ABCMeta):
    """Entry point to Entities with aggregate root role"""

    def __init__(self):
        """
        Initializes empty list of domain events
        """
        self._domain_events = []

    def pull_domain_events(self):
        """
        Pull stored domain events.

        @return: Current domain events
        """
        domain_events = self._domain_events
        self._domain_events = []
        return domain_events

    def record(self, domain_event):
        """
        Stores a new domain event.

        @param domain_event: new domain event to store
        @return: Nothing
        """
        self._domain_events.append(domain_event)
