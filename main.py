#EventAPI created by dannyx-hub @2022
import ssl
import datetime
import logging
from sqlite3 import Cursor
from flask import Flask,request,Response,abort,jsonify
from flask_restful import Api
from flask_mail import Mail,Message
from flask_cors import CORS
from Database import db
from config import emailconfig,appconfig
import hashlib
from art import tprint,decor
import jwt
from functools import wraps
import re

version = '1.1.1'
#-------------------------------------------------------------------------------------------------------
logging.basicConfig(format='%(message)s',stream=open(r'log.txt', 'w', encoding='utf-8'),level=5)
tprint("EventAPI")
logging.info(decor("barcode1") +f"    EventAPI version: {version} created by dannyx-hub    " + decor("barcode1",reverse=True))
print(decor("barcode1") +f"    version: {version} created by dannyx-hub   " + decor("barcode1",reverse=True))
print("\ngithub: https://github.com/dannyx-hub\n")
#-------------------------------------------------------------------------------------------------------
emailconfig = emailconfig()
appconfig = appconfig()
app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SECRET_KEY'] = appconfig['secret_key']
# app.config['DEBUG'] = appconfig['debug']
app.config['MAIL_SERVER']=emailconfig['server']
app.config['MAIL_PORT'] = emailconfig['port']
app.config['MAIL_USERNAME'] = emailconfig['username']
app.config['MAIL_PASSWORD'] = emailconfig['password']
# app.config['MAIL_USE_TLS'] = emailconfig['tls']
# app.config['MAIL_USE_SSL'] = emailconfig['ssl']
mail = Mail(app)
db = db()
db.BeginConnection()
#-------------------------------------------------------------------------------------------------------
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return("token missing")
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms="HS256")
        except Exception as e:
            print(e)
            return Response("invalid token",status=403)
        return f(*args,**kwargs)
    return decorator
#-------------------------------------------------------------------------------------------------------
#LOGIN sqldone
@app.route('/api/login', methods=['POST'])
def logowanie():
    
    login = request.form.get('login')
    password = request.form.get('haslo')
    logging.info(f"[*] Login attempt: {login,password}")
    test = hashlib.md5(password.encode())
    loginmatch = re.search('([\=\-\"\\\/\@\&])+',login)
    passwordmatch = re.search('([\=\-\"\\\/\@\&])+',password)
    if login == '' or password == '':
        return Response(status=402)
    else:
        if loginmatch or passwordmatch:
            logging.error("[!] REGEX TRIGGER")
            return Response(status=402)
        else:
            query = "select login,id,role from users where login =%s and hash =%s "
            data = (login,test.hexdigest())
            log = db.CursorExec(query,data)
            if len(log)==1:
                token = jwt.encode({'user':log[0][0],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
                logging.info(f"[*] Login succesfull: {login}")
                return jsonify({'token':token,'id':log[0][1],'role':log[0][2]})
            else:
                abort(403)
#-------------------------------------------------------------------------------------------------------
#REGISTER #sqldone
@app.route('/api/register',methods=['POST'] )
@token_required
def register():

    
    login = request.form.get('login')
    password = request.form.get('haslo')
    loginmatch = re.search('([\=\-\"\\\/\@\&])+',login)
    passwordmatch = re.search('([\=\-\"\\\/\@\&])+',password)
    logging.info(f"[*] register attempt: {login,password}")
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
        check = db.fetchOne(checkquery,data)
        if len(check)==1:
            return Response(status=409)
        else:
            query = f"insert into users(login,hash,role) values(%s,%s,'user')"
            data = (login,passwdhash.hexdigest())
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
    eventname = str(request.form.get('eventname'))
    eventpersoncreator = str(request.form.get('eventpersoncreator'))
    eventstartdate = request.form.get('eventstartdate')
    eventstopdate = request.form.get('eventstopdate')
    descr = str(request.form.get('descr'))
    email = request.form.get('email')
    approved = False
    if eventname =='' or eventpersoncreator == '' or eventstartdate == '' or eventname ==None or eventpersoncreator == None or eventstartdate == None:
        logging.error("[!] lecturesadd error!")
        return Response("zla data",status=409)
    else:
        if eventstartdate>eventstopdate:
            logging.error("[!] lecturesadd error! Bad date configuration")
            return Response("zla data",status=409)
        else:
            query = f"SELECT id from events where eventname = %s and eventstartdate = %s"
            data = (eventname,eventstartdate)
            checklog = db.CursorExec(query,data)
            if len(checklog) <=0:
                try:
                    sqlquery = """insert into events (eventname,eventstartdate,eventpersoncreator,approved,eventstopdate,descr,email) values(%s,%s,%s,%s,%s,%s,%s)"""
                    data = (eventname,eventstartdate,eventpersoncreator,approved,eventstopdate,descr,email)
                    # insert = db.InsertQuery("insert into events (eventname,eventstartdate,eventpersoncreator,approved,eventstopdate,descr,email) values('{eventname}','{eventstartdate}','{eventpersoncreator}','false','{eventstopdate}','\\{descr}','{email}')")
                    insert = db.InsertQuery(sqlquery,data)
                    if insert == True:
                        try:
                            msg = Message('Potwierdzenie dodania wydarzenia',sender ='no-reply-EventCalendar@dannyx123.ct8.pl',recipients = [email])
                            msg.html=f"<h3>Twoje wydarzenie:</h3>\n<h2>{eventname}</h2>\n<br><b>data</b>:{eventstartdate} - {eventstopdate}<br><b>opis</b>:{descr}\n<br>zostało utworzone i czeka na zatwierdzenie. Jego aktualny stan możesz sprawdzić na naszej <a href='http://129.159.203.123/'>stronie internetowej</a>"
                            mail.send(msg)
                            # print(msg)
                            logging.info("[*] Eventadd Mail send!")
                        except Exception as e:
                            logging.error(f"[!] Mail send ERROR : {e}")
                        logging.info("[*] lecturesadd add sucessfull!")
                        return Response('dodano prelekcje',status=200)
                    else:
                        logging.error("[!] lecturesadd exists!")
                        return Response('prelekcja istnieje',status=409)
                except Exception as e:
                    logging.error(f"[!] lecturesadd error: {e}")

                    abort(501)

            else:
                return Response(status=500)
#-------------------------------------------------------------------------------------------------------
#APPROVED EVENTS LIST
@app.route('/api/list',methods=['GET'])
def list():
    jsonobj = []
    columns = ["id","eventname","eventstartdate","eventstopdate","eventpersoncreator","descr","approved"]
    list = db.CursorExec('SELECT id,eventname,eventstartdate,eventstopdate,eventpersoncreator,descr,approved from events order by id desc')
    if list is None:
        return "[]"
    for x in range(len(list)):
       data={}
       for col in range(len(columns)):
           data[columns[col]]=list[x][col]
       jsonobj.append(data)
    return jsonify(jsonobj)

# @app.route("/api/remove", methods=['DELETE'])
# @token_required
# def remove():

#     body = request.get_json()
#     deletequery = f"delete from events where id={body['id']}"
#     delete = db.DeleteQuery(deletequery)
#     if delete == True:
#         logging.info("[*] event delete sucessfull!")
#         return Response("ok",status=200)
#     else:
#         return Response(status=404)
# #-------------------------------------------------------------------------------------------------------
#ROUTE TO LIST UNAPPROVED EVENTS AND APPROVE EVENT
@app.route('/api/approve',methods=['PUT','POST','DELETE'])
@token_required
def approve():
    if request.method == "PUT":
        jsonobj=[]
        selectnotapproved = "select id,eventname,eventstartdate,eventstopdate,eventpersoncreator,descr from events where approved = false"
        notapproved = db.CursorExec(selectnotapproved)
        if notapproved is None:
            return"[]"
        else:
            columns = ["id","eventname","eventstartdate","eventstopdate","eventpersoncreator","descr"]
            for x in range(len(notapproved)):
                data = {}
                for col in range(len(columns)):
                    data[columns[col]] = notapproved[x][col]
                jsonobj.append(data)
            return jsonify(jsonobj)
    elif request.method == "POST":
        body = request.get_json()
        checkquery = f'select eventname,eventstartdate,eventstopdate,descr,email from events where id =%s and approved = false'
        
        check = db.CursorExec(checkquery,[body['id']])
        if len(check)<1:
            return Response('{"msg":"bad id"}',status=500)
        elif len(check) == 1:
            updatequery = f"update events set approved = True where id = %s"
            data= body['id']
            update = db.UpdateQuery(updatequery,[data])
            if update == True:
                try:
                    msg = Message('Zmiana statusu wydarzenia',sender ='no-reply-EventCalendar@dannyx123.ct8.pl',recipients = [f'{check[0][4]}'])
                    msg.html=f"<h3>Twoje wydarzenie:</h3>\n<h2>{check[0][0]}</h2>\n<br><b>data</b>:{check[0][1]} - {check[0][2]}<br><b>opis</b>:{check[0][3]}\n<br>zmieniło status na <b><u>ZATWIERDZONY</u></b>.<br>Jego aktualny stan możesz sprawdzić na naszej <a href='http://129.159.203.123/'>stronie internetowej</a>"
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
        checkquery = f"select email,eventname,eventstartdate,eventstopdate,eventpersoncreator,descr from events where id = %s"
        data= body['id']
        deletequery = f"delete from events where id=%s"
        check = db.CursorExec(checkquery,[data])
        print(check)
        if len(check) == 1:
            delete = db.DeleteQuery(deletequery,[data])
            if delete == True:
                try:
                    msg = Message('Twoje wydarzenie zostało usunięte',sender='no-reply-EventCalendar@dannyx123.ct8.pl',recipients =[f'{check[0][0]}'])
                    msg.html=f"<h3>Twoje wydarzenie:</h3>\n<h2>{check[0][1]}</h2>\n<br><b>data</b>:{check[0][2]} - {check[0][3]}<br><b>opis</b>:{check[0][5]}\n<br>zmieniło status na <b><u>ODRZUCONY</u></b><br><b>powód:</b>{body['msg']}<br>Jego aktualny stan możesz sprawdzić na naszej <a href='http://129.159.203.123/'>stronie internetowej</a>"
                    # msg.body = "dupadupa123."
                    mail.send(msg)
                    logging.info("[*] Mail send!")
                except Exception as e:
                    logging.error(' [!] Mail send ERROR: ',e)
                logging.info("[*] event delete sucessfull!")
                return Response("ok",status=200)
            else:
                return Response(status=404)
        elif len(check)!=1:
            return(Response(status=402))    
    else:
        return Response(status=404)
#-------------------------------------------------------------------------------------------------------
#ROUTE TO LIST USERS,UPDATE ROLE AND DELETE THEM
@app.route('/api/user',methods=['POST','GET','DELETE'])
@token_required
def user():
    if request.method == 'GET':
        selectuserquery = "select id,login,role from users"
        columns = ['id','login','role']
        selecteduser = db.CursorExec(selectuserquery)
        if selecteduser is None:
            return "[]"
        jsonobj=[]
        for x in range(len(selecteduser)):
            data = {}
            for col in range(len(columns)):
                data[columns[col]] = selecteduser[x][col]
                
            jsonobj.append(data)
        return jsonify(jsonobj)
    elif request.method == "POST":
        body = request.get_json()
        updateQuery = f"Update users set role = 'root' where id=%s"
        data= body['id']
        update = db.UpdateQuery(updateQuery,data)
        if update == True:
            logging.info("[*] user update sucessfull!")
            return Response("ok",status=200)
        else:
            return Response(status=500)
    elif request.method == 'DELETE':
        body = request.get_json()
        deletequery = f"delete from users where id=%s"
        data= body['id']
        delete = db.DeleteQuery(deletequery,data)
        if delete == True:
            logging.info("[*] user delete sucessfull!")
            return Response("ok",status=200)
        else:
            return Response(status=500)
    else:
        return Response(status=500)
#-------------------------------------------------------------------------------------------------------
