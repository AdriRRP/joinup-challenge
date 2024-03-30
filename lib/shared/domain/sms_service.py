from abc import abstractmethod
from abc import ABCMeta


class SmsService(metaclass=ABCMeta):
    """Abstract sms service contract"""

    @abstractmethod
    def send(self, phone: str, message: str):
        """
        Sends a message with given `body` to `user_email`

        @param phone:    phone number to send sms
        @param message:  content of the sms
        @return: Nothing
        """
        pass
