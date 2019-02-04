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
''' 
event table name convention:
 -top_$eventuuid_$prjuuid: top level event details
 -det_$eventuuid_$prjuuid: detailed event list
'''
CURRENT_TIMESTAMP = "CURRENT_TIMESTAMP"

class eventDB:
    def __init__(self, usrid, prjid, eventName, desc, category):
        self.conn = psycopg2.connect(
        database=DBNAME,
        user=DBUSER,
        host=DBHOST,
        password=DBPASS
        )
        self.cur = self.conn.cursor()
        self.usrid = usrid
        self.prjid = prjid
        self.eventName = eventName
        self.desc = desc
        self.category = category

    def createEventUUID(self):
        event_id = str(uuid.uuid4())
        event_id_final = event_id[:5]
        self.eventid = event_id_final

    def createTopEventTable(self):
        table_nom = "top_%s_%s" % (self.eventid, self.prjid)
        self.eTopTable = table_nom
        par1 = "creator_uid VARCHAR(10)"
        par2 = "prj_uuid VARCHAR(5)"
        par3 = "name text"
        par4 = "date_created timestamp default CURRENT_TIMESTAMP"
        par5 = "date_mod timestamp"
        par6 = "event_id VARCHAR(5)"

        table_str = "CREATE TABLE %s (%s, %s, %s, %s, %s, %s REFERENCES %s(prj_uuid));" % (table_nom, par1, par3, par4, par5, par6, par2, pm_top)
        try:
            self.cur.execute(table_str)
            self.conn.commit()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0

    def createDetEventTable(self):
        table_nom = "det_%s_%s" % (self.eventid, self.prjid)
        self.eDetTable = table_nom
        par1 = "assignee VARCHAR(10)"
        par2 = "category VARCHAR(255)"
        par3 = "status int"
        par4 = "description text"
        par_ref = "prj_uuid VARCHAR(5)"

        table_str = "CREATE TABLE %s (%s, %s, %s, %s, %s REFERENCES %s(prj_uuid));" % (table_nom, par1, par2, par3, par4, par_ref, pm_top)
        try:
            self.cur.execute(table_str)
            self.conn.commit()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0

    def insertTopEventTable(self):
        insert_str = "INSERT INTO %s (creator_uid, name, date_mod, event_id, prj_uuid) VALUES ('%s', '%s', %s, '%s', '%s')" % (self.eTopTable, self.usrid, self.eventName, CURRENT_TIMESTAMP, self.eventid, self.prjid)
        try:
            self.cur.execute(insert_str)
            self.conn.commit()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0

    def insertDetEventTable(self):
        insert_str = "INSERT INTO %s (assignee, category, status, description, prj_uuid) VALUES ('%s', '%s', %d, '%s', '%s')" % (self.eDetTable, self.usrid, self.category, 2, self.desc, self.prjid)
        try:
            self.cur.execute(insert_str)
            self.conn.commit()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0

    def updateTopTable(self):
        check_str = "SELECT events FROM %s WHERE prj_uuid = '%s'" % (pm_top, self.prjid)
        event = None
        try:
            self.cur.execute(check_str)
            event = self.cur.fetchone()[0]
        except psycopg2.Error as e:
            print e.pgerror
            return None

        print 'event', event
        e_new = '' 
        if event is None:
            e_new = self.eventid
        else:
            e_new = "%s,%s"  % (event, self.eventid)
        print 'e_new', e_new

        update_str = "UPDATE %s SET events = '%s' WHERE prj_uuid = '%s'" % (pm_top, e_new, self.prjid)
        try:
            self.cur.execute(update_str)
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

    def createEvent(self):
        self.createEventUUID()
        self.createTopEventTable()
        self.createDetEventTable()

        self.insertTopEventTable()
        self.insertDetEventTable()

        #update top level
        self.updateTopTable()

        return self.eventid 


