import logging
from config.config import emailconfig
from flask_mail import Mail, Message

# TODO: maile sa spierdolone trzeba pomodzić z current_app bo czuje ze inaczej nie przejdzie
class Email:
    def __init__(self):
        from lecturesAPI.main import app
        logging.basicConfig(format='%(message)s', stream=open(r'log.txt', 'w', encoding='utf-8'), level=5)
        self.mail = Mail()
        app.debug = 0
        self.mail.init_app(app)
        config = emailconfig()
        # Mail server Config from Config.ini
        app.config['MAIL_SERVER'] = config['server']
        app.config['MAIL_PORT'] = config['port']
        app.config['MAIL_USERNAME'] = config['username']
        app.config['MAIL_PASSWORD'] = config['password']
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
        except Exception as e:
            logging.error("[!] Event email error: ", e)
