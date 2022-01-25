import psycopg2
from config import config
import logging
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

class db:
    def __init__(self):
        self.dbconfig = config()
        logging.basicConfig(filename='log.txt',level='DEBUG',filemode="a")
        self.force= None
    def BeginConnection(self):
        try:
            self.conn = psycopg2.connect(**self.dbconfig)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
            print("* Connected to Database")
            cursor = self.conn.cursor()
            # if self.force == None:
            #     with open('Event.sql','r') as sqlfile:
            #         tab = sqlfile.readlines()
            #         for x in range(len(tab)):
            #             print(tab[x])
            #             cursor.execute(tab[x])
            #             self.conn.commit()
            #             self.force = True
            #         print("* Dodano układ bazy")
            # else:
            #     print("* nic")       
            
        except Exception as e:
            print(e)


    def CursorExec(self,query):
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.cursor.close()
        return result
    
    def InsertQuery(self,query):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def UpdateQuery(self,query):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def DeleteQuery(self,query):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def run(self):
        self.BeginConnection()
        self.CursorExec()
