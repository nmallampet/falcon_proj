import os, sys

#psql adaptor 
import psycopg2



#DB VARS
DBNAME = "pmdb"
DBUSER = "user_admin"
DBPASS = "dbAdmin123"
DBHOST = "206.189.169.138"

#TABLE_NAMES
pm_top = "pm_top"




#connect to exisiting database and return cursor 'cur'
def establish_db_conn():
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
def create_pm_top(cur):
    par1 = "prj_uuid VARCHAR(5)"
    par2 = "prj_name text"
    par3 = "usr_uuid VARCHAR(10)"
    par4 = "date_created timestamp default CURRENT_TIMESTAMP"
    par5 = "date_mod timestamp"
    par6 = 'events text'
    table_str = "CREATE TABLE %s (%s, %s, %s, %s, %s, %s, PRIMARY KEY (prj_uuid));" % (pm_top, par1, par2, par3, par4, par5, par6)
    print table_str
    cur.execute(table_str)
    print "Created table successfully\n\n"

#create detailed user table
'''
def create_pm_users(cur):
    par1 = "prj_uuid VARCHAR(10)"
    par2 = "prj_uuid VARCHAR(10)"
    par3 = "fname VARCHAR(255)"
    par4 = "lname VARCHAR(255)"
    par5 = "type VARCHAR(255)"
    par6 = "email VARCHAR(255)"
    par7 = "phone VARCHAR(255)"
    table_str = "CREATE TABLE %s (%s, %s, %s, %s, %s, %s REFERENCES %s(prj_uuid));" % (pm_users, par2, par3, par4, par5, par6, par1, pm_top)
    print table_str
    cur.execute(table_str)
    print "Created table successfully\n\n"
'''

if __name__ == '__main__':
    conn, cur = establish_db_conn()

    #create user tables
    create_pm_top(cur)
    #create_pm_users(cur)

    #commit changes
    conn.commit()

    #close conn
    close_db_conn(conn, cur)
    print "All tables created and connections closed"
    exit(0)
        
