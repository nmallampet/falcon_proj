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


class getEventDetDB:
    def __init__(self, prjid):
        self.conn = psycopg2.connect(
        database=DBNAME,
        user=DBUSER,
        host=DBHOST,
        password=DBPASS
        )
        self.cur = self.conn.cursor()
        self.prjid = prjid

    def getAllEvents(self):
        get_str = "SELECT events FROM %s WHERE prj_uuid = '%s'" % (pm_top, self.prjid)
        try:
            self.cur.execute(get_str)
            self.events = self.cur.fetchone()[0]
        except psycopg2.Error as e:
            print e.pgerror

    def convertStatus(self, status):
        if status == 0:
            return 'Done'
        elif status == 1:
            return 'In progress'
        else:
            return "Not started"
            
    def getDetEvents(self):
        event_list = self.events.split(',')
        event_dict = {}
        for e in event_list:
            top_table = "top_%s_%s" % (e, self.prjid) #name, date_created, date_mod
            det_table = "det_%s_%s" % (e, self.prjid) #assignee, category, status, description
            get_str1 = "SELECT name, to_char(date_created, 'MM/dd/YYYY HH:MI:SS AM'), to_char(date_mod, 'MM/dd/YYYY HH:MI:SS AM') FROM %s WHERE prj_uuid = '%s'" % (top_table, self.prjid)
            try:
                self.cur.execute(get_str1)
                if self.cur.rowcount == 1:
                    prj_tuple = self.cur.fetchone()
                    event_name = prj_tuple[0]
                    date_created = prj_tuple[1]
                    date_mod = prj_tuple[2]
            except psycopg2.Error as e:
                print e.pgerror
            get_str2 = "SELECT assignee, category, status, description FROM %s WHERE prj_uuid = '%s'" % (det_table, self.prjid)
            try:
                self.cur.execute(get_str1)
                if self.cur.rowcount == 1:
                    prj_tuple2 = self.cur.fetchone()
                    assignee = prj_tuple2[0]
                    category = prj_tuple2[1]
                    status = self.convertStatus(prj_tuple2[2])
                    #description = prj_tuple2[3]
                    description = ''a
            except psycopg2.Error as e:
                print e.pgerror

            tmp_dict = {}
            tmp_dict['name'] = event_name
            tmp_dict['date_created'] = date_created
            tmp_dict['date_mod'] = date_mod
            tmp_dict['assignee'] = assignee
            tmp_dict['category'] = category
            tmp_dict['status'] = status
            tmp_dict['description'] = description

            event_dict[e] = tmp_dict

        return event_dict



    def closeConn(self):
        try:
            self.cur.close()
            self.conn.close()
        except psycopg2.Error as e:
            print e.pgerror
            return 1

        return 0


    def getEvents(self):
        self.getAllEvents()
        event_dict = self.getDetEvents()

        return self.events, event_dict

