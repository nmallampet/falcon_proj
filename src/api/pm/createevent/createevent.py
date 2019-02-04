import falcon
import json 

from createevent_db import eventDB


R_STAT = "status"
R_EUUID = "eventid"
R_MSG = "message"

class createevent:

    def on_options(self, req, res):
        res.status = falcon.HTTP_200
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header('Access-Control-Allow-Methods', 'POST')
        res.set_header('Access-Control-Allow-Headers', 'Content-Type')

    def on_post(self, req, resp):
        #get data
        data = json.loads(req.stream.read()) 

        #need:usrid, prjid, eventName, desc, category
        prjid = data['prjid']
        usrid = data['usrid']
        eventName = data['eventName']
        desc = data['desc']
        category = data['category']

        eventdb = eventDB(usrid, prjid, eventName, desc, category)
        eventID = eventdb.createEvent()

        ret_code = eventdb.closeConn()
        msg = ''

        if ret_code == 0:
            msg = "success"
        else:
            msg = "failure"

        output = {R_STAT:ret_code, R_MSG:msg, R_EUUID:eventID}

        #return status code
        resp.body = json.dumps(output, encoding='utf-8')

        if ret_code == 0:
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_500


