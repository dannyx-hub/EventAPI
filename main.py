from logging import NOTSET
from flask import Flask,request,Response,abort
from flask_restful import Api
from Database import db
import hashlib
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

@app.route('/api/list',methods=['POST'])
def list():
    list = db.CursorExec('SELECT eventname,eventdate,eventpersoncreator from events')
    for x in range(len(list)):
        return list[0][x]
    
app.run(host='0.0.0.0')