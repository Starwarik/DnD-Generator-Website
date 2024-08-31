import smtplib
from email.message import EmailMessage

from abc import ABC, abstractmethod

from app.notification.config import NotificationServiceChoice, notification_setting


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
    def __init__(self):
        pass

    def start(self):
        pass

    def send_refactory_notification(self, recciver_email, token):
        mail_server = smtplib.SMTP_SSL(
            notification_setting.smtp_server_url, notification_setting.smtp_server_port
        )
        mail_server.set_debuglevel(1)
        mail_server.login(
            notification_setting.smtp_login, notification_setting.smtp_password
        )
        mail_server.auth_plain()
        msg = EmailMessage()
        msg.set_content(notification_setting.smtp_template_message.format(token=token))

        msg["Subject"] = notification_setting.smtp_template_subject.format(token=token)
        msg["From"] = notification_setting.smtp_sender_email
        msg["To"] = recciver_email
        mail_server.send_message(msg)
        mail_server.quit()

    def stop(self):
        pass


notification_service = None

if (
    notification_setting.notification_service
    == NotificationServiceChoice.dummy_notification
):
    notification_service = DummyNotification()
elif (
    notification_setting.notification_service
    == NotificationServiceChoice.smtp_notification
):
    notification_service = SMTPNotification()
