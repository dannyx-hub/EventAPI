from logging import NOTSET
from flask import Flask,request,Response,abort,jsonify
from flask_restful import Api
from Database import db
import hashlib
import datetime
import json
app = Flask(__name__)
api = Api(app)
app.config['DEBUG'] = True
db = db()
db.BeginConnection()


@app.route('/api/login', methods=['POST'])
def logowanie():
    login = request.form.get('login')
    password = request.form.get('haslo')
    test = hashlib.md5(password.encode())
    print(test.hexdigest())
    if login == '' or password == '':
        return "podaj dane logowania"
    else:
        print(login,password)
        # return login, password
        query = f"select id from users where login ='{login}' and hash ='{test.hexdigest()}' "
        print(query)
        log = db.CursorExec(query)
        print(len(log))
        if len(log)==1:
            return "<h5>DZIALA</h5>"
        else:
            abort(403)


@app.route('/api/register',methods=['POST'] )
def register():
    login = request.form.get('login')
    password = request.form.get('haslo')
    if login == '' or password == '':
            return "podaj wszystkie dane"
    else:
        print(login,password)
        passwdhash = hashlib.md5(password.encode())
        query = f"insert into users(login,hash,role) values('{login}','{passwdhash.hexdigest()}','user')"
        exec = db.InsertQuery(query)
        if exec == True:
            return "Zarejestrowano użytkownika",200
        else:
            abort(404)

@app.route('/api/lecturesadd',methods = ['POST'])
def lecturesadd():
    name = request.form.get('name')
    who = request.form.get('who')
    when = request.form.get('when')
    print(name,who,when)
    if name =='' or who == '' or when == '':
       return Response(status=404)
    else:
        query = f"SELECT id from events where eventname = '{name}' and eventdate = '{when}'"
        checklog = db.CursorExec(query)
        print(len(checklog))
        if len(checklog) <=0:
            try:
                insert = db.InsertQuery(f"insert into events (eventname,eventdate,eventpersoncreator) values('{name}','{when}','{who}')")
                if insert == True:
                    return Response('dodano prelekcje',status=200)
                else:
                    return Response('prelekcja istnieje',status=404)
            except Exception as e:
                print(e)
                abort(404)

        else:
            return Response(status=404)

@app.route('/api/list',methods=['GET'])
def list():
    jsonobj = []
    columns = ["eventname","eventdate","eventpersoncreator"]
    list = db.CursorExec('SELECT eventname,eventdate,eventpersoncreator from events')
    print(list[0][1])
    print(len(list))
    for x in range(len(list)):
       data={}
       for col in range(len(columns)): 
           print(x,col)
        #    data ={
        #         columns[col]:list[x][col],
        #         f'eventdata':list[x][1],
        #         f'eventpersoncreator':list[x][2]
        #         }
           data[columns[col]]=list[x][col]
           jsonobj.append(data)
        

      
    return jsonify(jsonobj)
app.run(host='0.0.0.0',port=32402)
