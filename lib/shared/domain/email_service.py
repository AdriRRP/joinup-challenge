from abc import abstractmethod
from abc import ABCMeta


class EmailService(metaclass=ABCMeta):
    """Abstract email service contract"""

    @abstractmethod
    def send(self, email: str, body: str):
        """
        Sends a message with given `body` to `email`

        @param email: user that will receive the mail
        @param body:  content of the mail
        @return: Nothing
        """
        pass
