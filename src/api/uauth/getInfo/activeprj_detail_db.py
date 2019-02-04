import os, sys, uuid

#psql adaptor 
import psycopg2

#DB VARS
DBNAME = "pmdb"
DBUSER = "user_admin"
DBPASS = "dbAdmin123"
DBHOST = "206.189.169.138"

#TABLE_NAMES
pm_top = "pm_top"

class detProjDB:
    def __init__(self, prjid):
        self.conn = psycopg2.connect(
        database=DBNAME,
        user=DBUSER,
        host=DBHOST,
        password=DBPASS
        )
        self.cur = self.conn.cursor()
        self.prjid = prjid

	'''
		get details of project based on prj uuid
	'''
    def getDetails(self):
        get_str = "SELECT prj_name, to_char(date_created, 'MM/dd/YYYY HH:MI:SS AM'), to_char(date_mod, 'MM/dd/YYYY HH:MI:SS AM'), description FROM %s WHERE prj_uuid = '%s'" % (pm_top, self.prjid)
        msg = "failure"
        det_dict = {}
        try:
            self.cur.execute(get_str)
            if self.cur.rowcount == 1:
                prj_tuple = self.cur.fetchone()
                prj_name = prj_tuple[0]
                date_created = prj_tuple[1]
                date_mod = prj_tuple[2]
                desc = prj_tuple[3]
                
                det_dict['name'] = prj_name
                det_dict['date_created'] = date_created
                det_dict['date_modified'] = date_mod
                det_dict['desc'] = desc

                msg = "success"
                return det_dict
        except psycopg2.Error as e:
            print e.pgerror
            return det_dict

        return det_dict


    #close connections to db
    def closeConn(self):
        try:
            self.cur.close()
            self.conn.close()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0


    def getProjInfo(self):
        dec_dict = self.getDetails()
        return dec_dict


