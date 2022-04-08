
import logging
from config.config import emailconfig
from flask_mail import Mail, Message
from flask import Flask
class Email:
    def __init__(self):
        # from main import app
        logging.basicConfig(format='%(message)s', stream=open(r'log.txt', 'a', encoding='utf-8'), level=5)
        config = emailconfig()
        self.mailapp = Flask(__name__)
        self.mailapp.config['MAIL_SERVER'] = config['server']
        self.mailapp.config['MAIL_PORT'] = config['port']
        self.mailapp.config['MAIL_USERNAME'] = config['username']
        self.mailapp.config['MAIL_PASSWORD'] = config['password']
        # mailapp.config['MAIL_USE_TLS'] = config['tls']
        # mailapp.config['MAIL_USE_SSL'] = config['ssl']
        self.mail = Mail(self.mailapp)
        # self.mail.init_app(self.mailapp)


    def eventaddsend(self, name, start, stop, descr, recp):
        try:
            # self.mail.init_app(self.mailapp)
            msg = Message('Potwierdzenie dodania wydarzenia',
                          sender='no-reply-EventCalendar@dannyx123.ct8.pl', recipients=[recp])

            msg.html = f"<h3>Twoje wydarzenie:" \
                       f"</h3>\n<h2>{name}</h2>\n" \
                       f"<br><b>data</b>:{start} - {stop}<br>" \
                       f"<b>opis</b>:{descr}\n" \
                       f"<br>zosta&#321o utworzone i czeka na zatwierdzenie." \
                       f" Jego aktualny stan mo&#380esz sprawdzi&#262 na naszej" \
                       f" <a href='https://karczmarpg.tk'>stronie internetowej</a><br><b>" \
                       f"Pozdrawiamy<br>Zesp&#243&#322 ds. IT karczmarpg.tk</b>"

            self.mail.send(msg)
            logging.info("[*] Mail send!")
            return True
        except Exception as e:
            return e

    def eventapprove(self, name, start, stop, descr, recp):
        try:
            msg = Message('Zmiana statusu wydarzenia', sender='no-reply-EventCalendar@dannyx123.ct8.pl',
                          recipients=[recp])
            msg.html = f"<h3>Twoje wydarzenie:</h3>\n<h2>{name}</h2>\n<br><b>" \
                       f"data</b>:{start} - {stop}<br><b>opis</b>:{descr}\n" \
                       f"<br>zmieniło status na <b><u>ZATWIERDZONY</u>" \
                       f"</b>.<br>Jego aktualny stan możesz sprawdzić na naszej" \
                       f" <a href='https://karczmarpg.tk'>stronie internetowej</a><br><b>" \
                       f"Pozdrawiamy<br>Zespół ds. IT karczmarpg.tk</b>"
            print(msg)
            # self.mail.send(msg)
            logging.info("[*] Mail send!")
            return True
        except Exception as e:
            return e

    def eventdelete(self, name, start, stop, descr, recp, msg):
        try:
            msg = Message('Twoje wydarzenie zostało usunięte', sender='no-reply-EventCalendar@dannyx123.ct8.pl',
                          recipients=[recp])
            msg.html = f"<h3>Twoje wydarzenie:</h3>\n<h2>{name}</h2>\n<br><b>data</b>" \
                       f":{start} - {stop}<br><b>opis</b>:{descr}\n<br>zmieniło status na" \
                       f" <b><u>ODRZUCONY</u></b><br><b>powód:</b>{msg}<br>Jego aktualny" \
                       f" stan możesz sprawdzić na naszej <a href='https://karczmarpg.tk'>stronie internetowej" \
                       f"</a>"
            self.mail.send(msg)
            logging.info("[*] Mail send!")
            return True
        except Exception as e:
            return e
    def eventedit(self, name, start, stop, descr, recp):
        try:
            msg = Message('Twoje wydarzenie zostało zaktualizowane',
                          sender='no-reply-EventCalendar@dannyx123.ct8.pl', recipients=[recp])
            msg.html = f"<h3>Twoje wydarzenie:</h3>\n<h2>{name}</h2>\n" \
                       f"<br><b>data</b>:{start}" \
                       f"- {stop}<br><b>opis</b>:{descr}\n<br>zostało zaktualizowane.<br>" \
                       f"Jego aktualny stan możesz sprawdzić na naszej" \
                       f" <a href='https://karczmarpg.tk/'>stronie internetowej</a>" \
                       f"<br><b>Pozdrawiamy<br>Zespół ds. IT karczmarpg.tk</b>"
            self.mail.send(msg)
            logging.info("[*] Mail send!")
            return True
        except Exception as e:
            return e

    def approveMail(self, name, start, stop, descr, recp):
        try:
            msg = Message('Zmiana statusu wydarzenia', sender='no-reply-EventCalendar@dannyx123.ct8.pl',
                          recipients=[f'{recp}'])
            msg.html = f"<h3>Twoje wydarzenie:</h3>\n<h2>{name}</h2>\n<br><b>" \
                       f"data</b>:{start} - {stop}<br><b>opis</b>:{descr} \n" \
                       f"<br>zmieniło status na <b><u>ZATWIERDZONY</u>" \
                       f"</b>.<br>Jego aktualny stan możesz sprawdzić na naszej" \
                       f" <a href='https://karczmarpg.tk'>stronie internetowej</a><br><b>" \
                       f"Pozdrawiamy<br>Zespół ds. IT karczmarpg.tk</b>"
            self.mail.send(msg)
            logging.info("[*] Mail send!")
            return True
        except Exception as e:
            return e

    def deleteMail(self, name, start, stop, descr, recp, arg):
        try:
            msg = Message('Twoje wydarzenie zostało usunięte', sender='no-reply-EventCalendar@dannyx123.ct8.pl',
                          recipients=[f'{recp}'])
            msg.html = f"<h3>Twoje wydarzenie:</h3>\n<h2>{name}</h2>\n<br><b>data</b>" \
                       f":{start} - {stop}<br><b>opis</b>:{descr}\n<br>zmieniło status na" \
                       f" <b><u>ODRZUCONY</u></b><br><b>powód:</b>{arg}<br>Jego aktualny" \
                       f" stan możesz sprawdzić na naszej <a href='https://karczmarpg.tk'>stronie internetowej" \
                       f"</a>"
            self.mail.send(msg)
            return True
        except Exception as e:
            return e

