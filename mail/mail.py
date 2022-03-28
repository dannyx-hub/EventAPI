from config.config import emailconfig
from flask_mail import Mail, Message
from flask import Flask
# from main import app
import logging


class Email:
    def __init__(self):
        logging.basicConfig(format='%(message)s', stream=open(r'log.txt', 'w', encoding='utf-8'), level=5)
        emailapp = Flask(__name__)
        self.mail = Mail(emailapp)
        config = emailconfig()
        # Mail server Config from Config.ini
        emailapp.config['MAIL_SERVER'] = config['server']
        emailapp.config['MAIL_PORT'] = config['port']
        emailapp.config['MAIL_USERNAME'] = config['username']
        emailapp.config['MAIL_PASSWORD'] = config['password']
        emailapp.config['MAIL_USE_TLS'] = config['tls']
        emailapp.config['MAIL_USE_SSL'] = config['ssl']

    def eventaddsend(self, name, start, stop, descr, recp):
        try:
            msg = Message('Potwierdzenie dodania wydarzenia',
                          sender='no-reply-EventCalendar@dannyx123.ct8.pl', recipients=[recp])
            msg.html = f"<h3>Twoje wydarzenie:" \
                       f"</h3>\n<h2>{name}</h2>\n" \
                       f"<br><b>data</b>:{start} - {stop}<br>" \
                       f"<b>opis</b>:{descr}\n" \
                       f"<br>zostało utworzone i czeka na zatwierdzenie." \
                       f" Jego aktualny stan możesz sprawdzić na naszej" \
                       f" <a href='https://karczmarpg.tk'>stronie internetowej</a><br><b>" \
                       f"Pozdrawiamy<br>Zespół ds. IT karczmarpg.tk</b>"
            self.mail.send(msg)
        except Exception as e:
            logging.error("[!] Event email error: ", e)