import smtplib
from email.message import EmailMessage

from abc import ABC, abstractmethod

from .config import SMTPData, NotificationServiceChoice


class NotificationService(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def send_refactory_notification(self, recciver_email, token):
        pass

    @abstractmethod
    def stop(self):
        pass


class DummyNotification(NotificationService):
    def start(self):
        pass

    def send_refactory_notification(self, recciver_email, token):
        pass

    def stop(self):
        pass

class SMTPNotification(NotificationService):
    def __init__(self, smtp_data: SMTPData):
        self.smtp_data = smtp_data

        self.mail_server = None

    def start(self):
        self.mail_server = smtplib.SMTP_SSL(self.smtp_data.server_url, self.smtp_data.port)
        self.mail_server.set_debuglevel(1)
        self.mail_server.ehlo(self.smtp_data.login)
        self.mail_server.login(self.smtp_data.login, self.smtp_data.password)
        self.mail_server.auth_plain()

    def send_refactory_notification(self, recciver_email, token):
        msg = EmailMessage()
        msg.set_content(self.smtp_data.template_message.format(token=token))

        msg["Subject"] = self.smtp_data.template_subject.format(token=token)
        msg["From"] = self.smtp_data.sender_email
        msg["To"] = recciver_email
        self.mail_server.send_message(msg)

    def stop(self):
        self.mail_server.quit()


def create_notification_service(
    notification_choice: NotificationServiceChoice, smtp_data: SMTPData = None
) -> NotificationService:
    if notification_choice == NotificationServiceChoice.dummy_notification:
        return DummyNotification()
    elif notification_choice == NotificationServiceChoice.smtp_notification:
        return SMTPNotification(smtp_data)
