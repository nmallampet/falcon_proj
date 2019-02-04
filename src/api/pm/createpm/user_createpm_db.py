import os, sys, uuid

#psql adaptor 
import psycopg2

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

#to_char(CURRENT_TIMESTAMP, 'MM/dd/YYYY HH:MI:SS AM')


class uPMDB:
    def __init__(self, usrid, prjid):
        self.conn = psycopg2.connect(
        database=DBNAME,
        user=DBUSER,
        host=DBHOST,
        password=DBPASS
        )
        self.cur = self.conn.cursor()
        self.usrid = usrid
        self.prjid = prjid

    def existsPMtable(self):
        prj_check_str = "SELECT * FROM %s WHERE usr_uuid = '%s'" % (user_table_pm, self.usrid)
        try:
            self.cur.execute(prj_check_str)
            #count = int(self.cur.fetchone()[0])
            count = self.cur.fetchone()
            if count == None:
                return 0
        except psycopg2.Error as e:
            print e.pgerror
            return 2
            
        return 1


    def newPMentry(self):
        insert_str = "INSERT INTO %s(aprj, usr_uuid) VALUES ('%s', '%s');" % (user_table_pm, self.prjid, self.usrid)
        try:
            self.cur.execute(insert_str)
            self.conn.commit()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0


    def addPMentry(self):
        get_str = "SELECT aprj FROM %s where usr_uuid = '%s'" % (user_table_pm, self.usrid)
        aprj_val = None
        try:
            self.cur.execute(get_str)
            aprj_tuple = self.cur.fetchone()
            aprj_val = aprj_tuple[0]
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        #update string
        aprj_final = "%s,%s" % (aprj_val, self.prjid)

        #update table with value
        update_str = "UPDATE %s SET aprj = '%s' WHERE usr_uuid = '%s'" % (user_table_pm, aprj_final, self.usrid)
        try:
            self.cur.execute(update_str)
            self.conn.commit()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0  

    def getName(self):
        get_name_str = "SELECT fname, lname FROM %s WHERE usr_uuid = '%s'" % (user_table_det, self.usrid)
        try:
            self.cur.execute(get_name_str)
            if self.cur.rowcount == 1:
                name_tuple = self.cur.fetchone()
                fname = name_tuple[0]
                lname = name_tuple[1]
                return fname, lname
        except psycopg2.Error as e:
            print e.pgerror
            return None, None

        return None, None

    #close connections to db
    def closeConn(self):
        try:
            self.cur.close()
            self.conn.close()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0

    def createPMEntry(self):
        ret_code = self.existsPMtable()
        if ret_code == 0:
            self.newPMentry()
        elif ret_code == 1:
            self.addPMentry()
        else:
            print "Error in adding PM entry to user"

        



