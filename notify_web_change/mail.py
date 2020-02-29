import smtplib
import datetime

from settings import \
    SMTP_SERVER, SMTP_PORT, MAIL_ACCOUNT, MAIL_PASSWORD, NOTIFY_MAILS


class MailServer:
    def __init__(self):
        self.server = self._connect()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.server.quit()

    @staticmethod
    def _connect():
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.ehlo()
            server.starttls()
            server.login(MAIL_ACCOUNT, MAIL_PASSWORD)
            return server
        except Exception as e:
            print("Not able to connect. %s" % e)

    def _send_email(self, subject, body, dest):
        date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        msg = "From: %s\nSubject: %s\nDate: %s\n\n%s""" % (
            MAIL_ACCOUNT,
            subject,
            date,
            body,
        )
        self.server.sendmail(MAIL_ACCOUNT, dest, msg)
        print("%s - Notification change sent to %s" % (date, dest))

    def send_notification(self, web):
        subject = "%s has changed" % web
        body = "A change has been detected in your tracked website %s" % web
        for email in NOTIFY_MAILS.split(","):
            self._send_email(subject, body, email)
