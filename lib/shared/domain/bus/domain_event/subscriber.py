from abc import abstractmethod
from abc import ABCMeta


class Subscriber(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def subscribed_to() -> list[str]:
        pass
