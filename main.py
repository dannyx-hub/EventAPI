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

@app.route('/api/login', methods=['GET','POST'])
def logowanie():
    if request.method == "POST":
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
            if len(log)>0:
                return "Niepoprawne dane logowania", Response(status= 201)
            else:
                return "<h5>KUUUURWA DZIALA</h5>"
    else:
         return '''
           <form method="POST" href="192.168.0.107/api/login">
               <div><label>Language: <input type="text" name="login"></label></div>
               <div><label>Framework: <input type="text" name="haslo"></label></div>
               <input type="submit" value="Submit">
           </form>'''
@app.route('/api/register',methods=['GET','POST'] )
def register():
    wynik=db.CursorExec('SELECT * FROM USERS')
    return str(wynik) 

app.run(host='0.0.0.0')