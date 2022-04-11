import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from config.config import emailconfig


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

    def SendTestMail(self,sent_from,sent_to,subject,text,html):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sent_from
        msg["To"] = sent_to
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        msg.attach(part1)
        msg.attach(part2)

        try:
            self.smtp_server.sendmail(sent_from, sent_to, msg.as_string())
            return True
        except Exception as e:
            return e

