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

#default params
DEF_VERIFIED = 0

class signupDB:
    def __init__(self, email, fname, lname, pword):
        self.conn = psycopg2.connect(
        database=DBNAME,
        user=DBUSER,
        host=DBHOST,
        password=DBPASS
        )
        self.cur = self.conn.cursor()
        self.email = email
        self.fname = fname
        self.lname = lname
        self.pword = pword

    def checkEmail(self):
        email_check_str = "SELECT COUNT(email) from  %s WHERE email = '%s'" % (user_table_top, self.email)
        try:
            self.cur.execute(email_check_str)
            email_count = int(self.cur.fetchone()[0])
            if email_count == 0:
                return 0
        except psycopg2.Error as e:
            print e.pgerror
            return 1
            
        return 1

    def createUUID(self):
        usr_id = str(uuid.uuid4())
        usr_id_final = usr_id[:10]
        self.usrid = usr_id_final
        

    def updatetable(self):
        #db queries to create user
        insert_str1 = "INSERT INTO %s(usr_uuid, email, ver, password) VALUES ('%s', '%s', %s, '%s');" % (user_table_top, self.usrid, self.email, DEF_VERIFIED, self.pword)
        insert_str2 = "INSERT INTO %s(fname, lname, usr_uuid) VALUES ('%s', '%s', '%s');" % (user_table_det, self.fname, self.lname, self.usrid)

        #execute and commite queries
        try:
            self.cur.execute(insert_str1)
            self.cur.execute(insert_str2)
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

    def createUser(self):
        self.createUUID()
        ret_code = self.updatetable()
        return self.usrid, ret_code

