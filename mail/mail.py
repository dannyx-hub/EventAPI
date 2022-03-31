import logging
from config.config import emailconfig
from flask_mail import Mail, Message
from flask import current_app
# TODO https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask <- zaciagnaie configu maila z main
#https://stackoverflow.com/questions/57734132/flask-application-context-app-app-context-push-works-but-cant-get-with-ap
# TODO: maile sa spierdolone trzeba pomodzić z current_app bo czuje ze inaczej nie przejdzie
class Email:
    def __init__(self):
        # from main import app
        logging.basicConfig(format='%(message)s', stream=open(r'log.txt', 'w', encoding='utf-8'), level=5)
        self.mail = Mail()
        config = emailconfig()
        self.mail.init_app(current_app)
        # Mail server Config from Config.ini

        # app.config['MAIL_PORT'] = config['port']
        # app.config['MAIL_USERNAME'] = config['username']
        # app.config['MAIL_PASSWORD'] = config['password']
        # emailapp.config['MAIL_USE_TLS'] = config['tls']
        # emailapp.config['MAIL_USE_SSL'] = config['ssl']

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
            return True
        except Exception as e:
            return e
