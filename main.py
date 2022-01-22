
import datetime
from flask import Flask,request,Response,abort,jsonify
from flask_restful import Api
from Database import db
import hashlib
import jwt
from functools import wraps
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = '123123123adsasdasd'
app.config['DEBUG'] = True
db = db()
db.BeginConnection()
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.CursorExec(f"SELECT id FROM USERS WHERE ROLE={data['id']}")
            print("ez")
            print(current_user[0][0])
            return f(current_user[0][0], *args, **kwargs)
        except:
            return jsonify({'message': 'token is invalid'})
    return decorator

@app.route('/api/login', methods=['POST'])
def logowanie():
    login = request.form.get('login')
    password = request.form.get('haslo')
    test = hashlib.md5(password.encode())
    if login == '' or password == '':
        return "podaj dane logowania"
    else:
        query = f"select id from users where login ='{login}' and hash ='{test.hexdigest()}' "
        log = db.CursorExec(query)
        print(log[0][0])
        if len(log)==1:
            token = jwt.encode({'id':log[0][0],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
            return jsonify({'token':token})
        else:
            abort(403)


@app.route('/api/register',methods=['POST'] )
def register():
    login = request.form.get('login')
    password = request.form.get('haslo')
    if login == '' or password == '':
            return "podaj wszystkie dane"
    else:
        passwdhash = hashlib.md5(password.encode())
        query = f"insert into users(login,hash,role) values('{login}','{passwdhash.hexdigest()}','user')"
        exec = db.InsertQuery(query)
        if exec == True:
            return Response(status=201)
        else:
            abort(404)

@app.route('/api/lecturesadd',methods = ['POST'])
def lecturesadd():
    name = request.form.get('name')
    who = request.form.get('who')
    when = request.form.get('when')
    if name =='' or who == '' or when == '':
       return Response(status=409)
    else:
        query = f"SELECT id from events where eventname = '{name}' and eventdate = '{when}'"
        checklog = db.CursorExec(query)
        if len(checklog) <=0:
            try:
                insert = db.InsertQuery(f"insert into events (eventname,eventstartdate,eventpersoncreator,approved,eventstopdate) values('{name}','{when}','{who}')")
                if insert == True:
                    return Response('dodano prelekcje',status=200)
                else:
                    return Response('prelekcja istnieje',status=409)
            except Exception as e:
                print(e)
                abort(404)

        else:
            return Response(status=404)

@app.route('/api/list',methods=['GET'])
@token_required
def list():
    jsonobj = []
    columns = ["eventname","eventstartdate","eventstopdata","eventpersoncreator"]
    list = db.CursorExec('SELECT eventname,eventstartdate,eventstopdata,eventpersoncreator from events where approved = True')
    for x in range(len(list)):
       data={}
       for col in range(len(columns)):
           data[columns[col]]=list[x][col]
       jsonobj.append(data)
    return jsonify(jsonobj)

@app.route('/api/approve',methods=['POST'])
def approve():
    print("approve")
    return "dupa"
app.run(host='0.0.0.0',port=32402)
