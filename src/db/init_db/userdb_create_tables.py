import os, sys

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


#connect to exisiting database and return cursor 'cur'
def establish_db_conn():
    #con_str = "dbname=%s user=%s" % (DBNAME, DBUSER)
    #conn = psycopg2.connect(con_str)
    conn = psycopg2.connect(
        database=DBNAME,
        user=DBUSER,
	host=DBHOST,
        password=DBPASS
        )
    cur = conn.cursor()
    return conn, cur

def close_db_conn(conn, cur):
    cur.close()
    conn.close()



#create top level table 
def create_table_top(cur):
    par1 = "id SERIAL"
    par2 = "usr_uuid VARCHAR(10)"
    par3 = "email VARCHAR(255)"
    par4 = "ver int"
    par5 = "password text NOT NULL"
    table_str = "CREATE TABLE %s (%s, %s, %s, %s, %s, PRIMARY KEY (usr_uuid));" % (user_table_top, par1, par2, par3, par4, par5)
    print table_str
    cur.execute(table_str)
    print "Created table successfully\n\n"

#create detailed user table
def create_table_det(cur):
    par1 = "usr_uuid VARCHAR(10)"
    par2 = "fname VARCHAR(255)"
    par3 = "lname VARCHAR(255)"
    par4 = "gender int"
    par5 = "age int"
    par6 = "phone VARCHAR(255)"
    table_str = "CREATE TABLE %s (%s, %s, %s, %s, %s, %s REFERENCES %s(usr_uuid));" % (user_table_det, par2, par3, par4, par5, par6, par1, user_table_top)
    print table_str
    cur.execute(table_str)
    print "Created table successfully\n\n"

#create pm user table
def create_table_pm(cur):
    par1 = "aprj text"
    par2 = "iprj text"
    par3 = "usr_uuid VARCHAR(10)"
    table_str = "CREATE TABLE %s (%s, %s, %s REFERENCES %s(usr_uuid));" % (user_table_pm, par1, par2, par3, user_table_top)
    print table_str
    cur.execute(table_str)
    print "Created table successfully\n\n"

#create group user table
def create_table_gid(cur):
    par1 = "gid text"
    par2 = "usr_uuid VARCHAR(10)"
    table_str = "CREATE TABLE %s (%s, %s REFERENCES %s(usr_uuid));" % (user_table_grps, par1, par2, user_table_top)
    print table_str
    cur.execute(table_str)
    print "Created table successfully\n\n"


if __name__ == '__main__':
    conn, cur = establish_db_conn()

    #create user tables
    create_table_top(cur)
    create_table_det(cur)
    create_table_pm(cur)
    create_table_gid(cur)

    #commit changes
    conn.commit()

    #close conn
    close_db_conn(conn, cur)
    print "All tables created and connections closed"
    exit(0)
        
