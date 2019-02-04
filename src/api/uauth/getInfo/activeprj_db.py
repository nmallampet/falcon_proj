import os, sys, uuid

#psql adaptor 
import psycopg2
from activeprj_detail_db import detProjDB
#DB VARS
DBNAME = "userdb"
DBUSER = "user_admin"
DBPASS = "dbAdmin123"
DBHOST = "206.189.169.138"

#TABLE_NAMES
user_table_top = "user_top"
user_table_det = "user_profile"
user_table_pm = "user_pm"
user_table_grps = "user_grps"


class aprjDB:
    def __init__(self, usrid):
        self.conn = psycopg2.connect(
        database=DBNAME,
        user=DBUSER,
        host=DBHOST,
        password=DBPASS
        )
        self.cur = self.conn.cursor()
        self.usrid = usrid


    def getReqData(self):
        get_str1 = "SELECT aprj, iprj FROM %s WHERE usr_uuid = '%s'" % (user_table_pm, self.usrid)
        msg = "failure"
        try:
            self.cur.execute(get_str1)
            if self.cur.rowcount == 1:
                prj_tuple = self.cur.fetchone()
                aprj = prj_tuple[0]
                iprj = prj_tuple[1]
                msg = "success"
                return aprj, iprj, msg
        except psycopg2.Error as e:
            print e.pgerror
            return None, None, msg

        return None, None, msg

    def getDetails(self, aprj, iprj):
        aprj_dict = {}
        iprj_dict = {}
        if aprj is not None:
            aprj_list = aprj.split(',')
            for a in aprj_list:
                dTmp = detProjDB(a)
                data = dTmp.getProjInfo()
                dTmp.closeConn()
                aprj_dict[a] = data

        if iprj is not None:
            iprj_list = iprj.split(',')
            for b in iprj_list:
                dTmp = detProjDB(b)
                data = dTmp.getProjInfo()
                dTmp.closeConn()
                iprj_dict[b] = data

        
        return aprj_dict, iprj_dict





    #close connections to db
    def closeConn(self):
        try:
            self.cur.close()
            self.conn.close()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0

    def getPrjs(self):
        aprj, iprj, msg = self.getReqData()
        aprj_dict, iprj_dict = self.getDetails(aprj, iprj)
        return aprj, iprj, msg, aprj_dict, iprj_dict

