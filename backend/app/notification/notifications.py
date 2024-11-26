import smtplib
from email.message import EmailMessage

from abc import ABC, abstractmethod

from app.notification.config import NotificationServiceChoice, notification_setting


class NotificationService(ABC):
    """
    Абстрактный класс для отправки письмо о сбросе пароля.
    """

    @abstractmethod
    def start(self):
        """
        Метод запускается в начале приложения. Нужен для некоторых сервисов для запуска.
        """

        pass

    @abstractmethod
    def send_refactory_notification(self, recciver_email: str, token: str):
        """
        Метод запускается в конце приложения. Нужен для некоторых сервисов, чтобы завершить какие-то процессы.
        :param recciver_email: почта пользователя, которому нужно отправить письмо.
        :param token: токен для сброса пароля. Если перейти по ссылке с ним, то сайт его определит и перейдет на форму сброса.
        """

        pass

    @abstractmethod
    def stop(self):
        """
        Метод запускается в конце приложения. Нужен для некоторых сервисов, чтобы завершить какие-то процессы.
        """

        pass


class DummyNotification(NotificationService):
    """
    Класс для отправки письмо о сбросе пароля.. Ничего не делает и является затычкей для тестирования.
    """

    def start(self):
        """
        Метод запускается в начале приложения. Нужен для некоторых сервисов для запуска.
        """

        pass

    def send_refactory_notification(self, recciver_email, token):
        """
        Метод запускается в конце приложения. Нужен для некоторых сервисов, чтобы завершить какие-то процессы.
        :param recciver_email: почта пользователя, которому нужно отправить письмо.
        :param token: токен для сброса пароля. Если перейти по ссылке с ним, то сайт его определит и перейдет на форму сброса.
        """
        pass

    def stop(self):
        pass


class SMTPNotification(NotificationService):
    """
    Класс для отправки письмо о сбросе пароля по протоколу SMTP.
    """

    def __init__(self):
        pass

    def start(self):
        """
        Метод запускается в начале приложения. Нужен для некоторых сервисов для запуска.
        """
        pass

    def send_refactory_notification(self, recciver_email, token):
        """
        Метод запускается в конце приложения. Нужен для некоторых сервисов, чтобы завершить какие-то процессы. Отправляет письмо по протоколу SMTP SSL, по шаблону указоному в notification_setting.
        :param recciver_email: почта пользователя, которому нужно отправить письмо.
        :param token: токен для сброса пароля. Если перейти по ссылке с ним, то сайт его определит и перейдет на форму сброса.
        """

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
        """
        Метод запускается в конце приложения. Нужен для некоторых сервисов, чтобы завершить какие-то процессы.
        """
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
