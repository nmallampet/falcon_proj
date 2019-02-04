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


class loginDB:
    def __init__(self, email, pword):
        self.conn = psycopg2.connect(
        database=DBNAME,
        user=DBUSER,
        host=DBHOST,
        password=DBPASS
        )
        self.cur = self.conn.cursor()
        self.email = email
        self.pword = pword

    def getUUID(self):
        get_usr_uid_str = "SELECT usr_uuid FROM %s WHERE email = '%s'" % (user_table_top, self.email)
        try:
            self.cur.execute(get_usr_uid_str)
            if self.cur.rowcount == 1:
                obtained_uuid = self.cur.fetchone()[0]
                return obtained_uuid
        except psycopg2.Error as e:
            print e.pgerror
            return None

        return None

    def getName(self, uuid):
        get_name_str = "SELECT fname, lname FROM %s WHERE usr_uuid = '%s'" % (user_table_det, uuid)
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

    
    def getPassAuth(self):
        get_usr_pass_str = "SELECT password FROM %s WHERE email = '%s'" % (user_table_top, self.email)
        try:
            self.cur.execute(get_usr_pass_str)
            if self.cur.rowcount == 1:
                obtained_pass = self.cur.fetchone()[0]
                if obtained_pass == self.pword:
                    return True
        except psycopg2.Error as e:
            print e.pgerror
            return False

        return False

    #close connections to db
    def closeConn(self):
        try:
            self.cur.close()
            self.conn.close()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0

    def confirmUser(self):
        correctPass = self.getPassAuth()
        if correctPass:
            usrid = self.getUUID()
            fname, lname = self.getName(usrid)
        else:
            usrid = None
            fname = None
            lname = None

        return correctPass, usrid, fname, lname
