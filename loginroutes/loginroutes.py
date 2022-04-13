from flask import request, Response, abort, jsonify, Blueprint
from datetime import datetime, timedelta
from config.config import appconfig
from functools import wraps
from database.Database import db
from mail.mail import NewEmail
import hashlib
import logging
import jwt

login_route = Blueprint('loginroute', __name__)
db = db()
db.BeginConnection()
config = appconfig()
mail = NewEmail()


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return "token missing"
        try:
            data = jwt.decode(token, config['secret_key'], algorithms="HS256")
        except Exception as e:
            print(e)
            return Response("invalid token", status=403)
        return f(*args, **kwargs)

    return decorator


@login_route.route("/api/approved", methods=['PUT', 'POST', 'DELETE'])
@token_required
def approve():
    if request.method == "PUT":
        body = request.get_json()
        checkexist = db.CursorExec("select id from events where id = %s", [body['id']])
        if len(checkexist) == 1:
            checkIfNewExist = db.CursorExec("select id from events where eventname= %s and id != %s",
                                            [body['eventname'], body['id']])
            if len(checkIfNewExist) == 0:
                updateEvent = db.UpdateQuery(
                    "update events set eventname = %s,eventstartdate= %s,eventstopdate= %s,eventpersoncreator= %s," \
                    "descr= %s,email= %s where id = %s ",
                    [body['eventname'], body['evenstartdate'], body['eventstopdate'],
                     body['eventpersoncreator'], body['descr'], body['email'], body['id']])
                if updateEvent is True:
                    try:
                        updateMail = mail.SendMail(body['eventname'], body['evenstartdate'], body['eventstopdate'],
                                                    body['descr'], body['email'])
                    except Exception:
                        logging.error("[!] Event Update mail Error: ", updateMail)
                    return Response(status=200)
                else:
                    logging.error("[!] Event update Error")
                    return Response(status=500)
            else:
                logging.error("[!] event update error, name event exist")
                return Response('{"msg":"event update error, name event exist"}', status=409)
        else:
            logging.error("[!] event update error, name event doesn't exist")
            return Response('{"msg":"event update error, name event doesnt exist"}', status=409)

    elif request.method == "POST":
        body = request.get_json()
        checkexist = db.CursorExec(
            "select eventname,eventstartdate,eventstopdate,descr,email from events where id =%s and "
            "approved = false ", [body['id']])
        print(checkexist)
        if len(checkexist) == 1:
            approveEvent = db.UpdateQuery("update events set approved = True where id = %s", [body['id']])
            if approveEvent is True:
                try:
                    approveMail = mail.approveMail(body['eventname'], body['evenstartdate'], body['eventstopdate'],
                                                   body['descr'], body['email'])
                except Exception:
                    logging.error("[!] Event Approve mail Error: ", approveMail)
            else:
                logging.error("[!] Event Approve error")
                return Response(status=500)
        else:
            logging.error("[!] Event Approve error - event dosent exist")
            return Response('{"msg":"Event Approve error, event doesnt exist"}', status=409)
    elif request.method == "DELETE":
        body = request.get_json()
        checkexist = db.CursorExec("select email,eventname,eventstartdate,eventstopdate,eventpersoncreator,descr"
                                   " from events where id= %s ", [body['id']])
        if len(checkexist) == 1:
            delete = db.DeleteQuery("delete from events where id= %s", [body['id']])
            if delete is True:
                try:
                    deleteMail = mail.deleteMail(body['eventname'], body['evenstartdate'], body['eventstopdate'],
                                                 body['descr'], body['email'], body['msg'])
                except Exception:
                    logging.error("[!] Event Delete mail Error: ", deleteMail)
                return Response(status=200)
            else:
                logging.error("[!] Event Delete error")
                return Response(status=500)
        else:
            logging.error("[!] event delete error, event doesn't exist")
            return Response('{"msg":"event delete error, event doesnt exist"}', status=409)
