import psycopg2
from config import config
import logging
class db:
    def __init__(self):
        self.dbconfig = config()
        logging.basicConfig(filename='log.txt',level='DEBUG',filemode="a")
        
    def BeginConnection(self):
        try:
            self.conn = psycopg2.connect(**self.dbconfig)
            print("Connected to Database")
        except Exception as e:
            print(e)
    def CursorExec(self,query):
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.cursor.close()
        return result

    def run(self):
        self.BeginConnection()
        self.CursorExec()


# db = db()
# db.run()
# db.BeginConnection()
# query = db.CursorExec('select * from event')
# print(query)