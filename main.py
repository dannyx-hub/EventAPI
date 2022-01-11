from logging import NOTSET
from flask import Flask,request,Response
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
            return "Niepoprawne dane logowania"


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
            return "Zarejestrowano użytkownika"
        else:
            return "Nie udało sie zarejestrować użytkownika"


app.run(host='0.0.0.0')