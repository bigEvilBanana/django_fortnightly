from abc import ABC, abstractmethod


class NotificationProvider(ABC):

    @staticmethod
    @abstractmethod
    def notify(to: str, message: str, *args, **kwargs):
        ...


class PushNotificationProvider(NotificationProvider):

    @staticmethod
    def notify(to: str, message: str, *args, **kwargs):
        print(f'PUSH: to {to}: {message}')


class EmailNotificationProvider(NotificationProvider):

    @staticmethod
    def notify(to: str, message: str, *args, **kwargs):
        print(f'EMAIL: to {to}: {message}')
