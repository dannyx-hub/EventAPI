import logging
from config.config import emailconfig
from flask_mail import Mail, Message
from flask import Flask
# TODO https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask <- zaciagnaie configu maila z main
#https://stackoverflow.com/questions/57734132/flask-application-context-app-app-context-push-works-but-cant-get-with-ap
# TODO: maile sa spierdolone trzeba pomodzić z current_app bo czuje ze inaczej nie przejdzie
class Email:
    def __init__(self):
        # from main import app
        logging.basicConfig(format='%(message)s', stream=open(r'log.txt', 'w', encoding='utf-8'), level=5)
        mailapp = Flask(__name__)
        self.mail = Mail()
        config = emailconfig()
        self.mail.init_app(mailapp)
        # Mail server Config from Config.ini

        mailapp.config['MAIL_PORT'] = config['port']
        mailapp.config['MAIL_USERNAME'] = config['username']
        mailapp.config['MAIL_PASSWORD'] = config['password']
        mailapp.config['MAIL_USE_TLS'] = config['tls']
        mailapp.config['MAIL_USE_SSL'] = config['ssl']

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
            mail.send(msg)
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
            mail.send(msg)
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
            mail.send(msg)
            logging.info("[*] Mail send!")
            return True
        except Exception as e:
            return e

    def approveMail(self,name,start,stop,descr,recp):
        try:
            msg = Message('Zmiana statusu wydarzenia', sender='no-reply-EventCalendar@dannyx123.ct8.pl',
                          recipients=[f'{recp}'])
            msg.html = f"<h3>Twoje wydarzenie:</h3>\n<h2>{name}</h2>\n<br><b>" \
                       f"data</b>:{start} - {stop}<br><b>opis</b>:{descr} \n" \
                       f"<br>zmieniło status na <b><u>ZATWIERDZONY</u>" \
                       f"</b>.<br>Jego aktualny stan możesz sprawdzić na naszej" \
                       f" <a href='https://karczmarpg.tk'>stronie internetowej</a><br><b>" \
                       f"Pozdrawiamy<br>Zespół ds. IT karczmarpg.tk</b>"
            mail.send(msg)
            logging.info("[*] Mail send!")
            return True
        except Exception as e:
            return e

    def deleteMail(self,name,start,stop,descr,recp,arg):
        try:
            msg = Message('Twoje wydarzenie zostało usunięte', sender='no-reply-EventCalendar@dannyx123.ct8.pl',
                          recipients=[f'{recp}'])
            msg.html = f"<h3>Twoje wydarzenie:</h3>\n<h2>{name}</h2>\n<br><b>data</b>" \
                       f":{start} - {stop}<br><b>opis</b>:{descr}\n<br>zmieniło status na" \
                       f" <b><u>ODRZUCONY</u></b><br><b>powód:</b>{arg}<br>Jego aktualny" \
                       f" stan możesz sprawdzić na naszej <a href='https://karczmarpg.tk'>stronie internetowej" \
                       f"</a>"
            mail.send(msg)
            return True
        except Exception as e:
            return e

