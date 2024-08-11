import smtplib
from email.message import EmailMessage

from abc import ABC, abstractmethod


class NotificationRefactory(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def send_refactory_notification(self, recciver_email, token):
        pass

    @abstractmethod
    def stop(self):
        pass


class DummyNotification(NotificationRefactory):
    def start(self):
        pass

    def send_refactory_notification(self, recciver_email, token):
        pass

    def stop(self):
        pass


class SMTPNotification(NotificationRefactory):
    def __init__(
        self,
        server_url: str,
        server_port: int,
        sender_email: str,
        login: str,
        password: str,
        template_subject: str,
        template_message: str,
    ):
        self.server_url = server_url
        self.server_port = server_port
        self.sender_email = sender_email
        self.login = login
        self.password = password
        self.template_subject = template_subject
        self.template_message = template_message

        self.mail_server = None

    def start(self):
        self.mail_server = smtplib.SMTP(self.server_url, self.server_port)
        self.mail_server.starttls()
        self.mail_server.login(self.login, self.password)

    def send_refactory_notification(self, recciver_email, token):
        msg = EmailMessage()
        msg.set_content(self.template_message.format(token=token))

        msg["Subject"] = self.template_subject.format(token=token)
        msg["From"] = self.sender_email
        msg["To"] = recciver_email
        self.mail_server.send_message(msg)

    def stop(self):
        self.mail_server.quit()
