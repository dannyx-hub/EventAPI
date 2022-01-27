#EventAPI version 1.0.2 created by dannyx-hub @2022

import datetime
import logging
from flask import Flask,request,Response,abort,jsonify
from flask_restful import Api
from flask_cors import CORS
from Database import db
import hashlib
from art import tprint,decor
import jwt
from functools import wraps

#-------------------------------------------------------------------------------------------------------
logging.basicConfig(format='%(message)s',stream=open(r'log.txt', 'w', encoding='utf-8'),level=5)
app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SECRET_KEY'] = '12312123123123secretkey123123123123'
app.config['DEBUG'] = True
db = db()
db.BeginConnection()

#-------------------------------------------------------------------------------------------------------

tprint("EventsAPI")
logging.info(decor("barcode1") +"    EventAPI version: 1.0.3 created by dannyx-hub    " + decor("barcode1",reverse=True))
print(decor("barcode1") +"    version: 1.0.3 created by dannyx-hub   " + decor("barcode1",reverse=True))
print("\ngithub: https://github.com/dannyx-hub\n")

#-------------------------------------------------------------------------------------------------------

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return("token missing")
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms="HS256")
            print(data['user'])
        except Exception as e:
            print(e)
            return "nie dziala"
        return f(*args,**kwargs)
    return decorator

#-------------------------------------------------------------------------------------------------------

#LOGIN
@app.route('/api/login', methods=['POST'])
def logowanie():
    
    login = request.form.get('login')
    password = request.form.get('haslo')
    logging.info(f"[*] Login attempt: {login,password}")
    test = hashlib.md5(password.encode())
    if login == '' or password == '':
        return "podaj dane logowania"
    else:
        query = f"select login from users where login ='{login}' and hash ='{test.hexdigest()}' "
        log = db.CursorExec(query)
        if len(log)==1:
            token = jwt.encode({'user':log[0][0],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
            logging.info(f"[*] Login succesfull: {login}")
            return jsonify({'token':token})
        else:
            abort(403)

#-------------------------------------------------------------------------------------------------------

#REGISTER
@app.route('/api/register',methods=['POST'] )
def register():
    
    login = request.form.get('login')
    password = request.form.get('haslo')
    logging.info(f"[*] register attempt: {login,password}")
    if login == '' or password == '':
            logging.error(f"[!] register error: blank inputs!")
            return "podaj wszystkie dane"

    else:
        passwdhash = hashlib.md5(password.encode())
        checkquery = f"select login from users where login ='{login}'"
        check = db.CursorExec(checkquery)
        if len(check)==1:
            return Response(status=409)
        else:
            query = f"insert into users(login,hash,role) values('{login}','{passwdhash.hexdigest()}','user')"
            exec = db.InsertQuery(query)
            if exec == True:
                logging.info(f"[*] register success!")
                return Response(status=201)
            else:
                logging.error("[!] register error")
                abort(404)

#-------------------------------------------------------------------------------------------------------

#ADD EVENT
@app.route('/api/eventadd',methods = ['POST'])
def lecturesadd():
    eventname = request.form.get('eventname')
    eventpersoncreator = request.form.get('eventpersoncreator')
    eventstartdate = request.form.get('eventstartdate')
    eventstopdate = request.form.get('eventstopdate')
    descr = request.form.get('descr')
    if eventname =='' or eventpersoncreator == '' or eventstartdate == '' or eventname ==None or eventpersoncreator == None or eventstartdate == None:
        logging.error("[!] lecturesadd error!")
        return Response("zla data",status=409)
    else:
        if eventstartdate>eventstopdate:
            logging.error("[!] lecturesadd error! Bad date configuration")
            return Response("zla data",status=409)
        else:
            query = f"SELECT id from events where eventname = '{eventname}' and eventstartdate = '{eventstartdate}'"
            checklog = db.CursorExec(query)
            if len(checklog) <=0:
                try:
                    insert = db.InsertQuery(f"insert into events (eventname,eventstartdate,eventpersoncreator,approved,eventstopdate,descr) values('{eventname}','{eventstartdate}','{eventpersoncreator}','false','{eventstopdate}','{descr}')")
                    if insert == True:
                        logging.info("[*] lecturesadd add sucessfull!")
                        return Response('dodano prelekcje',status=200)
                    else:
                        logging.error("[!] lecturesadd exists!")
                        return Response('prelekcja istnieje',status=409)
                except Exception as e:
                    logging.error(f"[!] lecturesadd error: {e}")

                    abort(501)

            else:
                return Response(status=404)

#-------------------------------------------------------------------------------------------------------

#APPROVED EVENTS LIST
@app.route('/api/list',methods=['GET'])
def list():
    jsonobj = []
    columns = ["eventname","eventstartdate","eventstopdate","eventpersoncreator","descr"]
    list = db.CursorExec('SELECT eventname,eventstartdate,eventstopdate,eventpersoncreator,descr from events where approved = True')
    for x in range(len(list)):
       data={}
       for col in range(len(columns)):
           data[columns[col]]=list[x][col]
       jsonobj.append(data)
    return jsonify(jsonobj)

#-------------------------------------------------------------------------------------------------------

#ROUTE TO LIST UNAPPROVED EVENTS AND APPROVE EVENT
@app.route('/api/approve',methods=['GET','POST'])
@token_required
def approve():
    if request.method == "GET":
        jsonobj=[]
        selectnotapproved = "select id,eventname,eventstartdate,eventstopdate,eventpersoncreator,descr from events where approved = false"
        notapproved = db.CursorExec(selectnotapproved)
        columns = ["id","eventname","eventstartdate","eventstopdate","eventpersoncreator","descr"]
        for x in range(len(notapproved)):
            data = {}
            for col in range(len(columns)):
                data[columns[col]] = notapproved[x][col]
                print(data)
            jsonobj.append(data)
        return jsonify(jsonobj)
    elif request.method == "POST":
        body = request.get_json()
        checkquery = f'select approved from events where id = {body["id"]} and approved = False'
        check = db.CursorExec(checkquery)
        if len(check) !=1:
            return Response('{"msg":"bad id"}',status=500)
        elif len(check) == 1:
            updatequery = f"update events set approved = True where id = {body['id']}"
            update = db.UpdateQuery(updatequery)
            if update == True:
                return Response(status=200)
            else:
                return Response(status=500)
        else:
            return Response(status=500)

#-------------------------------------------------------------------------------------------------------

#ROUTE TO LIST USERS,UPDATE ROLE AND DELETE THEM
@app.route('/api/user',methods=['POST','GET','DELETE'])
@token_required
def user():
    if request.method == 'GET':
        selectuserquery = "select id,login,role from users"
        columns = ['id','login','role']
        selecteduser = db.CursorExec(selectuserquery)
        jsonobj=[]
        for x in range(len(selecteduser)):
            data = {}
            for col in range(len(columns)):
                data[columns[col]] = selecteduser[x][col]
                
            jsonobj.append(data)
        return jsonify(jsonobj)
    elif request.method == "POST":
        body = request.get_json()
        updateQuery = f"Update users set role = 'root' where id={body['id']}"
        update = db.UpdateQuery(updateQuery)
        if update == True:
            return Response("ok",status=200)
        else:
            return Response(status=500)
    elif request.method == 'DELETE':
        body = request.get_json()
        deletequery = f"delete from users where id={body['id']}"
        delete = db.DeleteQuery(deletequery)
        if delete == True:
            return Response("ok",status=200)
        else:
            return Response(status=500)
    else:
        return Response(status=500)

#-------------------------------------------------------------------------------------------------------