import os, sys, uuid

#psql adaptor 
import psycopg2

from user_createpm_db import uPMDB

#DB VARS
DBNAME = "pmdb"
DBUSER = "user_admin"
DBPASS = "dbAdmin123"
DBHOST = "206.189.169.138"

#TABLE_NAMES
pm_top = "pm_top"

#to_char(CURRENT_TIMESTAMP, 'MM/dd/YYYY HH:MI:SS AM')
CURRENT_TIMESTAMP = "CURRENT_TIMESTAMP"

class pmDB:
    def __init__(self, prjname, usrid):
        self.conn = psycopg2.connect(
        database=DBNAME,
        user=DBUSER,
        host=DBHOST,
        password=DBPASS
        )
        self.cur = self.conn.cursor()
        self.prjname = prjname
        self.usrid = usrid


    def createPrjUUID(self):
        prj_id = str(uuid.uuid4())
        prj_id_final = prj_id[:5]
        self.prjid = prj_id_final


    def updateUsertable(self):
        upm = uPMDB(self.usrid, self.prjid)
        fname, lname = upm.getName()
        upm.createPMEntry()
        upm.closeConn()
        return fname, lname
        

    def updateToptable(self):
        #db queries to create user
        insert_str1 = "INSERT INTO %s(prj_uuid, prj_name, usr_uuid, date_mod) VALUES ('%s', '%s', '%s', %s);" % (pm_top, self.prjid, self.prjname, self.usrid, CURRENT_TIMESTAMP)

        #execute and commite queries
        try:
            self.cur.execute(insert_str1)
            self.conn.commit()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0


    def createUsersTable(self):
        table_str = "users_%s" % (self.prjid)
        self.userTable = table_str
        par1 = "usr_uuid VARCHAR(10)"
        par2 = "prj_uuid VARCHAR(5)"
        par3 = "fname VARCHAR(255)"
        par4 = "lname VARCHAR(255)"
        par5 = "type VARCHAR(255)"
        par6 = "email VARCHAR(255)"
        par7 = "phone VARCHAR(255)"
        create_table_str = "CREATE TABLE %s (%s, %s, %s, %s, %s, %s, %s REFERENCES %s(prj_uuid))" % (table_str, par1, par3, par4, par5, par6, par7, par2, pm_top)

        try:
            self.cur.execute(create_table_str)
            self.conn.commit()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0


    def updatePMUsertable(self):
        insert_str1 = "INSERT INTO %s(usr_uuid, fname, lname, type, prj_uuid) VALUES ('%s', '%s', '%s', '%s', '%s')" % (self.userTable, self.usrid, self.fname, self.lname, "admin", self.prjid)
        try:
            self.cur.execute(insert_str1)
            self.conn.commit()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0


    #close connections to db
    def closeConn(self):
        try:
            self.cur.close()
            self.conn.close()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0

    def createPM(self):
        #create prjID
        self.createPrjUUID()

        #update userdb
        fname, lname = self.updateUsertable()
        self.fname = fname
        self.lname = lname

        #create entries in PM DB
        self.updateToptable()
        self.createUsersTable()
        self.updatePMUsertable()

        return self.prjid


        

