import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import emailconfig


class NewEmail:
    # https://realpython.com/python-send-email/#starting-a-secure-smtp-connection
    def __init__(self):
        mailconfig = emailconfig()
        self.server = mailconfig['server']
        self.port = mailconfig['port']
        self.username = mailconfig['username']
        self.password = mailconfig['password']

    def beginConnection(self):
        self.smtp_server = smtplib.SMTP(self.server, self.port)
        try:
            self.smtp_server.ehlo()
            self.smtp_server.login(self.username, self.password)
            return True
        except Exception as e:
            print(e)

    def SendTestMail(self, charset='utf-8'):
        sent_from = "no-reply-EventCalendar@dannyx123.ct8.pl"
        to = ['damian.paluch0503@gmail.com']
        subject = 'Test nowego maila'
        body = "ążźćęóń"
        email_text = """\
                From: %s
                To: %s
                Subject: %s
                %s
                """ % (sent_from, ", ".join(to), subject, body)
        try:
            self.smtp_server.sendmail(sent_from, to, email_text.encode("utf8"))
            print("dziala")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    test = newEmail()
    test.beginConnection()
    if test.beginConnection() is True:
        test.SendTestMail()
