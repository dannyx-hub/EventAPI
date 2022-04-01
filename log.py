from datetime import datetime
from flask import request
import logging

class Log:
    def __init__(self):
        today = datetime.now()
        self.today_format = today.strftime("%G-%m-%d")


    def listlog(self,path,con):
        ip = request.remote_addr
        data = [ip,path,self.today_format]
        logquery = "insert into log(ip,path,data) values(%s,%s,%s)"
        savelog = con.InsertQuery(logquery,data)
        if savelog is True:
            pass
        else:
            logging.warning("[?] List log error")
            raise Exception


    def Eventaddlog(self,path,con):
        ip = request.remote_addr
        data = [ip, path, self.today_format]
        logquery = "insert into log(ip,path,data) values(%s,%s,%s)"
        savelog = con.InsertQuery(logquery, data)
        if savelog is True:
            pass
        else:
            logging.warning("[?] List log error")
            raise Exception
