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
        if login == '' or password == '':
            return "podaj dane logowania"
        else:
            print(login,password)
            # return login, password
            query = f"select login from users where login ='{login}' and hash ='{password}' "
            print(query)
            log = db.CursorExec(query)
            if log is None:
                return "Niepoprawne dane logowania", Response(status= 201)
            else:
                return "udalo sie"
    else:
         return '''
           <form method="POST">
               <div><label>Language: <input type="text" name="login"></label></div>
               <div><label>Framework: <input type="text" name="haslo"></label></div>
               <input type="submit" value="Submit">
           </form>'''
@app.route('/api/register',methods=['GET','POST'] )
app.run()