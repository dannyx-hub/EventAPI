# EventAPI created by dannyx-hub @2022

from datetime import datetime, timedelta
import logging
from time import strftime
from flask import Flask, request, Response, abort, jsonify
from flask_restful import Api
from flask_mail import Mail, Message
from flask_cors import CORS
from database.Database import db
from config.config import emailconfig, appconfig
import hashlib
from art import tprint, decor
import jwt
from functools import wraps
import re
from userroutes.userroute import user_route

version = '2.0.1'
# -------------------------------------------------------------------------------------------------------

logging.basicConfig(format='%(message)s', stream=open(r'log.txt', 'w', encoding='utf-8'), level=5)
tprint("EventAPI")
logging.info(
    decor("barcode1") + f"    EventAPI version: {version} created by dannyx-hub    " + decor("barcode1", reverse=True))
print(decor("barcode1") + f"    version: {version} created by dannyx-hub   " + decor("barcode1", reverse=True))
print("\ngithub: https://github.com/dannyx-hub\n")
# -------------------------------------------------------------------------------------------------------
emailconfig = emailconfig()
appconfig = appconfig()
app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SECRET_KEY'] = appconfig['secret_key']
# app.config['DEBUG'] = appconfig['debug']
app.config['MAIL_SERVER'] = emailconfig['server']
app.config['MAIL_PORT'] = emailconfig['port']
app.config['MAIL_USERNAME'] = emailconfig['username']
app.config['MAIL_PASSWORD'] = emailconfig['password']
# app.config['MAIL_USE_TLS'] = emailconfig['tls']
# app.config['MAIL_USE_SSL'] = emailconfig['ssl']
mail = Mail(app)
db = db()
db.BeginConnection()
app.register_blueprint(user_route)


# -------------------------------------------------------------------------------------------------------
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return "token missing"
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        except Exception as e:
            print(e)
            return Response("invalid token", status=403)
        return f(*args, **kwargs)

    return decorator


# -------------------------------------------------------------------------------------------------------
# LOGIN sqldone
@app.route('/api/login', methods=['POST'])
def logowanie():
    today = datetime.now()
    today_format = today.strftime("%G-%m-%d")
    iplog = request.remote_addr
    path = "api/list"
    data = [iplog, path, today_format]
    logquery = "insert into log(ip,path,data) values (%s,%s,%s)"
    savelog = db.InsertQuery(logquery, data)
    if savelog is True:
        pass
    else:
        pass
    login = request.form.get('login')
    password = request.form.get('haslo')
    logging.info(f"[*] Login attempt: {login, password}")
    test = hashlib.md5(password.encode())
    loginmatch = re.search('([\=\-\"\\\/\@\&])+', login)
    passwordmatch = re.search('([\=\-\"\\\/\@\&])+', password)
    if login == '' or password == '':
        return Response(status=402)
    else:
        if loginmatch or passwordmatch:
            logging.error("[!] REGEX TRIGGER")
            return Response(status=402)
        else:
            query = "select login,id,role from users where login =%s and hash =%s "
            data = (login, test.hexdigest())
            log = db.CursorExec(query, data)
            if len(log) == 1:
                token = jwt.encode({'user': log[0][0], 'exp': datetime.utcnow() + timedelta(minutes=45)},
                                   app.config['SECRET_KEY'], "HS256")
                logging.info(f"[*] Login succesfull: {login}")
                return jsonify({'token': token, 'id': log[0][1], 'role': log[0][2]})
            else:
                abort(403)


# -------------------------------------------------------------------------------------------------------
# REGISTER #sqldone
@app.route('/api/register', methods=['POST'])
@token_required
def register():
    today = datetime.now()
    today_format = today.strftime("%G-%m-%d")
    iplog = request.remote_addr
    path = "api/list"
    data = [iplog, path, today_format]
    logquery = "insert into log(ip,path,data) values (%s,%s,%s)"
    savelog = db.InsertQuery(logquery, data)
    if savelog is True:
        pass
    else:
        pass
    login = request.form.get('login')
    password = request.form.get('haslo')
    loginmatch = re.search('([\=\-\"\\\/\@\&])+', login)
    passwordmatch = re.search('([\=\-\"\\\/\@\&])+', password)
    logging.info(f"[*] register attempt: {login, password}")
    if login == '' or password == '':
        logging.error(f"[!] register error: blank inputs!")
        return Response(status=402)

    else:
        if loginmatch or passwordmatch:
            logging.error("[!] REGEX TRIGGER")
            return Response(status=402)
        passwdhash = hashlib.md5(password.encode())
        checkquery = f"select login from users where login =%s"
        data = login
        check = db.fetchOne(checkquery, data)
        if len(check) == 1:
            return Response(status=409)
        else:
            query = f"insert into users(login,hash,role) values(%s,%s,'user')"
            data = (login, passwdhash.hexdigest())
            exec = db.InsertQuery(query)
            if exec is True:
                logging.info(f"[*] register success!")
                return Response(status=201)
            else:
                logging.error("[!] register error")
                abort(404)


# ------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# ROUTE TO LIST UNAPPROVED EVENTS AND APPROVE EVENT
@app.route('/api/approve', methods=['PUT', 'POST', 'DELETE'])
@token_required
def approve():
    if request.method == "PUT":
        body = request.get_json()
        checkquery = "select id from events where id =%s"
        putid = body['id']
        check = db.CursorExec(checkquery, [putid])
        if len(check) == 1:
            eventname = body['eventname']
            eventstartdate = body['eventstartdate']
            eventstopdate = body['eventstopdate']
            eventpersoncreator = body['eventpersoncreator']
            descr = body['descr']
            email = body['email']
            checkifexistquery = "select id from events where eventname = %s and id != %s  "
            checkifexistdata = [eventname, putid]
            checkifexist = db.CursorExec(checkifexistquery, checkifexistdata)
            updatequery = "update events set eventname = %s,eventstartdate=%s,eventstopdate=%s,eventpersoncreator=%s," \
                          "descr=%s,email=%s where id = %s "
            print(len(checkifexist))
            if len(checkifexist) == 0:
                data = (eventname, eventstartdate, eventstopdate, eventpersoncreator, descr, email, putid)
                update = db.UpdateQuery(updatequery, data)
                if update is True:
                    logging.info("[*] Event Update")
                    try:
                        msg = Message('Twoje wydarzenie zostało zaktualizowane',
                                      sender='no-reply-EventCalendar@dannyx123.ct8.pl', recipients=[email])
                        msg.html = f"<h3>Twoje wydarzenie:</h3>\n<h2>{eventname}</h2>\n" \
                                   f"<br><b>data</b>:{eventstartdate}" \
                                   f"- {eventstopdate}<br><b>opis</b>:{descr}\n<br>zostało zaktualizowane.<br>" \
                                   f"Jego aktualny stan możesz sprawdzić na naszej" \
                                   f" <a href='https://karczmarpg.tk/'>stronie internetowej</a>" \
                                   f"<br><b>Pozdrawiamy<br>Zespół ds. IT karczmarpg.tk</b>"
                        mail.send(msg)
                    except Exception as e:
                        logging.error("[!] PUT mail error: ", e)

                    return Response(status=200)
                else:
                    logging.error("[!] event update error")
                    return Response(status=409)

            else:
                logging.error("[!] event update error, name event exist")
                return Response('{"msg":"event update error, name event exist"}', status=409)
    # else:
    #     logging.error("[!] event update error")
    #     return Response(status=402)
    elif request.method == "POST":
        body = request.get_json()
        checkquery = f'select eventname,eventstartdate,eventstopdate,descr,email from events where id =%s and ' \
                     f'approved = false '

        check = db.CursorExec(checkquery, [body['id']])
        if len(check) < 1:
            return Response('{"msg":"bad id"}', status=500)
        elif len(check) == 1:
            updatequery = f"update events set approved = True where id = %s"
            data = body['id']
            update = db.UpdateQuery(updatequery, [data])
            if update is True:
                try:
                    msg = Message('Zmiana statusu wydarzenia', sender='no-reply-EventCalendar@dannyx123.ct8.pl',
                                  recipients=[f'{check[0][4]}'])
                    msg.html = f"<h3>Twoje wydarzenie:</h3>\n<h2>{check[0][0]}</h2>\n<br><b>" \
                               f"data</b>:{check[0][1]} - {check[0][2]}<br><b>opis</b>:{check[0][3]}\n" \
                               f"<br>zmieniło status na <b><u>ZATWIERDZONY</u>" \
                               f"</b>.<br>Jego aktualny stan możesz sprawdzić na naszej" \
                               f" <a href='https://karczmarpg.tk'>stronie internetowej</a><br><b>" \
                               f"Pozdrawiamy<br>Zespół ds. IT karczmarpg.tk</b>"
                    mail.send(msg)
                    logging.info("[*] Mail send!")
                except Exception as e:
                    logging.error(f"[!] Mail send ERROR : {e}")

                logging.info("[*] event update sucessfull!")

                return Response(status=200)
            else:
                return Response(status=500)
    elif request.method == "DELETE":
        body = request.get_json()
        checkquery = f"select email,eventname,eventstartdate,eventstopdate,eventpersoncreator,descr " \
                     f"from events where " \
                     f"id = %s "
        data = body['id']
        deletequery = f"delete from events where id=%s"
        check = db.CursorExec(checkquery, [data])
        print(check)
        if len(check) == 1:
            delete = db.DeleteQuery(deletequery, [data])
            if delete is True:
                try:
                    msg = Message('Twoje wydarzenie zostało usunięte', sender='no-reply-EventCalendar@dannyx123.ct8.pl',
                                  recipients=[f'{check[0][0]}'])
                    msg.html = f"<h3>Twoje wydarzenie:</h3>\n<h2>{check[0][1]}</h2>\n<br><b>data</b>" \
                               f":{check[0][2]} - {check[0][3]}<br><b>opis</b>:{check[0][5]}\n<br>zmieniło status na" \
                               f" <b><u>ODRZUCONY</u></b><br><b>powód:</b>{body['msg']}<br>Jego aktualny" \
                               f" stan możesz sprawdzić na naszej <a href='https://karczmarpg.tk'>stronie internetowej"\
                               f"</a>"
                    mail.send(msg)
                    logging.info("[*] Mail send!")
                except Exception as e:
                    logging.error(' [!] Mail send ERROR: ', e)
                logging.info("[*] event delete sucessfull!")
                return Response("ok", status=200)
            else:
                return Response(status=404)
        elif len(check) != 1:
            return Response(status=402)
    else:
        return Response(status=404)


# -------------------------------------------------------------------------------------------------------
# ROUTE TO LIST USERS,UPDATE ROLE AND DELETE THEM
@app.route('/api/user', methods=['POST', 'GET', 'DELETE'])
@token_required
def user():
    if request.method == 'GET':
        selectuserquery = "select id,login,role from users"
        columns = ['id', 'login', 'role']
        selecteduser = db.CursorExec(selectuserquery)
        if selecteduser is None or len(selecteduser) == 0:
            return "[]"
        jsonobj = []
        for x in range(len(selecteduser)):
            data = {}
            for col in range(len(columns)):
                data[columns[col]] = selecteduser[x][col]

            jsonobj.append(data)
        return jsonify(jsonobj)
    elif request.method == "POST":
        body = request.get_json()
        updateQuery = f"Update users set role = 'root' where id=%s"
        data = body['id']
        update = db.UpdateQuery(updateQuery, data)
        if update is True:
            logging.info("[*] user update sucessfull!")
            return Response("ok", status=200)
        else:
            return Response(status=500)
    elif request.method == 'DELETE':
        body = request.get_json()
        deletequery = f"delete from users where id=%s"
        data = body['id']
        delete = db.DeleteQuery(deletequery, data)
        if delete is True:
            logging.info("[*] user delete sucessfull!")
            return Response("ok", status=200)
        else:
            return Response(status=500)
    else:
        return Response(status=500)


@app.route("/api/log", methods=['GET'])
# @token_required
def log():
    printquery = "select id,ip,path,data from log"
    ipcountquery = f"select count(ip) from log where data = %s"
    data = []
    jsonobj = []
    columns = ['id', 'ip', 'path', 'data']
    # ipcount = db.CursorExec(ipcountquery,data)
    log = db.CursorExec(printquery, data)
    iplog = db.CursorExec(ipcountquery, datetime.now())
    if log is None or len(log) == 0:
        return "[]"
    else:
        for x in range(len(log)):
            data = {}
            for col in range(len(columns)):
                data[columns[col]] = log[x][col]
            jsonobj.append(data)
        return jsonify(jsonobj)


# -------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    debug = appconfig['debug']
    if debug == "True":
        print("* API port: ", appconfig['devport'])
        app.run(host=appconfig['host'], port=appconfig['devport'])
    elif debug == "False":
        print("* API port: ", appconfig['port'])
        app.run(host=appconfig['host'], port=appconfig['port'], ssl_context=("server.pem", "server.key"))
