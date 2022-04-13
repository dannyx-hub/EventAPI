import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import emailconfig


class NewEmail:
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

    def parseMail(self, template, name, start, stop, descr, ifDelete=False, comment=None):
        with open(template, "r") as templatefile:
            checkfile = str(templatefile.read())
        if ifDelete is True:
            message = checkfile.format(EventName=name, startDate=start, stopDate=stop, EventDescr=descr, Comment=comment)
        else:
            message = checkfile.format(EventName=name, startDate=start, stopDate=stop, EventDescr=descr)
        return message

    def SendMail(self, sent_to, subject, template, name, start, stop, descr, isDelete, comment):
        sent_from = "no-reply-EventCalendar@dannyx123.ct8.pl"
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sent_from
        msg["To"] = sent_to
        html = self.parseMail(template, name, start, stop, descr, isDelete, comment)
        part = MIMEText(html, "html")
        msg.attach(part)

        try:
            self.smtp_server.sendmail(sent_from, sent_to, msg.as_string())
            return True

        except Exception as e:
            return e



# mail = NewEmail()
# mail.beginConnection()
# mail.SendMail("damian.paluch0503@gmail.com", "test maila", './template/EventAdd.html', "eventname", "2022-04-21", "2022-04-22", "test", False, None)