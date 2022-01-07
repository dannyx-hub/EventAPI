from flask import Flask,jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
#config
DEBUG = True
#instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

#cors
CORS(app, resources={r'/*': {'origins': '*'}})

#check if works
@app.route('/ping',methods = ['GET'])
def ping_pong():
    return jsonify("pong!")


if __name__ == '__main__':
    app.run()