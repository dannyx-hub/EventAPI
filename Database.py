import psycopg2
from config import config
import logging
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

class db:
    def __init__(self):
        self.dbconfig = config()
        logging.basicConfig(filename='log.txt',level='DEBUG',filemode="a")
        
    def BeginConnection(self):
        try:
            self.conn = psycopg2.connect(**self.dbconfig)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
            print("* Connected to Database")
            cursor = self.conn.cursor()
            # with open('Event.sql','r') as sqlfile:
            #     tab = sqlfile.readlines()
            #     for x in range(len(tab)):
            #         print(tab[x])
            #         cursor.execute(tab[x])
            #         self.conn.commit()
            #     print("* Dodano układ bazy")
                
            
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
