import hashlib
import logging
import re
from datetime import datetime, timedelta
import jwt
from mail.mail import NewEmail
from config.config import appconfig
from database.Database import db
from flask import request, Response, abort, jsonify, Blueprint
from log import Log

user_route = Blueprint('userroute', __name__)
mail = NewEmail()
db = db()
db.BeginConnection()
mail.beginConnection()
config = appconfig()
config['SECRET_KEY'] = config['secret_key']
log = Log()

"""list route: - generate json object with all events, check parameter archived  if true return all finished events 
false all unfinished events 
use in EventCalendar package """


@user_route.route('/api/list', methods=['GET'])
def list():
    # TODO zapiski do logów muszą mieć funkcje z parametrem (path)
    archived = request.args.get('archived')
    today = datetime.now()
    today_format = today.strftime("%G-%m-%d")
    log.Addlog('/api/log', db)
    jsonobj = []
    columns = ["id", "eventname", "eventstartdate", "eventstopdate", "eventpersoncreator", "email", "descr", "approved"]
    if archived == "false":
        list = db.CursorExec(
            'SELECT id,eventname,eventstartdate,eventstopdate,eventpersoncreator,email,descr,approved '
            'from events where eventstopdate >= %s order by id desc',
            [today_format])
        if list is None or len(list) == 0:
            return "[]"
        for x in range(len(list)):
            data = {}
            for col in range(len(columns)):
                data[columns[col]] = list[x][col]
            jsonobj.append(data)
        return jsonify(jsonobj)
    elif archived == "true":
        list = db.CursorExec(
            'SELECT id,eventname,eventstartdate,eventstopdate,'
            'eventpersoncreator,email,descr,approved from events '
            'where eventstopdate < %s order by id desc',
            [today_format])
        if list is None or len(list) == 0:
            return "[]"
        for x in range(len(list)):
            data = {}
            for col in range(len(columns)):
                data[columns[col]] = list[x][col]
        jsonobj.append(data)
        return jsonify(jsonobj)


@user_route.route('/api/eventadd', methods=['POST'])
def lecturesadd():
    today = datetime.now()
    today_format = today.strftime("%G-%m-%d")
    log.Addlog('/api/eventadd', db)
    eventname = str(request.form.get('eventname'))
    eventpersoncreator = str(request.form.get('eventpersoncreator'))
    eventstartdate = request.form.get('eventstartdate')
    eventstopdate = request.form.get('eventstopdate')
    descr = str(request.form.get('descr'))
    email = request.form.get('email')
    approved = False
    if not eventname or eventpersoncreator == '' or eventstartdate == '' or eventname is None \
            or eventpersoncreator is None or eventstartdate is None:
        logging.error("[!] lecturesadd error!")
        return Response(status=409)
    else:
        if eventstartdate > eventstopdate:
            logging.error("[!] lecturesadd error! Bad date configuration")
            return Response(status=409)
        else:
            query = f"SELECT id from events where eventname = %s and eventstartdate = %s"
            data = (eventname, eventstartdate)
            checklog = db.CursorExec(query, data)
            if len(checklog) <= 0:
                try:
                    sqlquery = "insert into events (eventname,eventstartdate,eventpersoncreator,approved," \
                               "eventstopdate,descr,email) values(%s,%s,%s,%s,%s,%s,%s) "
                    data = (eventname, eventstartdate, eventpersoncreator, approved, eventstopdate, descr, email)
                    insert = db.InsertQuery(sqlquery, data)
                    if insert is True:
                        try:
                            test = mail.SendMail(email, "Wydarzenie zostało utworzone", './mail/template/EventAdd.html', eventname, eventstartdate, eventstopdate, descr, False,None)
                        except Exception as e:
                            logging.error(f"[!] Mail send ERROR : {e}")
                        logging.info("[*] lecturesadd add sucessfull!")
                        return Response('dodano prelekcje', status=200)
                    else:
                        logging.error("[!] lecturesadd exists!")
                        return Response('event exists', status=409)
                except Exception as e:
                    logging.error(f"[!] lecturesadd error: {e}")

                    abort(501)
            else:
                return Response(status=500)


@user_route.route("/api/login", methods=['POST'])
def logowanie():
    login = request.form.get('login')
    password = request.form.get('haslo')
    logging.info(f"[*] Login attempt: {login, password}")
    test = hashlib.md5(password.encode())
    loginmatch = re.search('([\=\-\"\\\/\@\&])+', login)
    passwordmatch = re.search('([\=\-\"\\\/\@\&])+', password)
    log.Addlog('/api/login', db)
    if login == '' or password == '':
        return Response(status=402)
    else:
        if loginmatch or passwordmatch:
            logging.error("[!] REGEX TRIGGER")
            return Response(status=402)
        else:
            query = "select login,id,role from users where login =%s and hash =%s "
            data = (login, test.hexdigest())
            loginQuery = db.CursorExec(query, data)
            if len(loginQuery) == 1:
                token = jwt.encode({'user': loginQuery[0][0], 'exp': datetime.utcnow() + timedelta(minutes=45)},
                                   config['SECRET_KEY'], "HS256")
                logging.info(f"[*] Login succesfull: {login}")
                return jsonify({'token': token, 'id': loginQuery[0][1], 'role': loginQuery[0][2]})
            else:
                abort(403)
