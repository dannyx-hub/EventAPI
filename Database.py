import psycopg2
from config import dbconfig
import logging
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

class db:
    def __init__(self):
        self.dbconfig = dbconfig()
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


    def CursorExec(self,sql,data=""):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql,data)
        result = self.cursor.fetchall()
        self.cursor.close()
        return result

    def fetchOne(self,sql,data=""):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql,data)
        if self.cursor.rowcount == 0:
            return 0
        else:
            result = self.cursor.fetchone()
            if result is None:
                return 0 
            else:
                self.cursor.close()
                return result
    def InsertQuery(self,sql,data=""):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql,data)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def UpdateQuery(self,sql,data=""):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql,data)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def DeleteQuery(self,sql,data=""):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql,data)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def run(self):
        self.BeginConnection()
        self.CursorExec()
