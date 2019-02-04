import falcon
import json 

from getEvents_db import getEventDetDB

R_STAT = "status"
R_EUUID = "eventuuid_list"
R_DE = "event_details"
R_MSG = "message"


class getEvents:
    def on_options(self, req, res):
        res.status = falcon.HTTP_200
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header('Access-Control-Allow-Methods', 'POST')
        res.set_header('Access-Control-Allow-Headers', 'Content-Type')

    def on_post(self, req, resp):
        #get data
        data = json.loads(req.stream.read()) 

        #need:usrid
        prjid = data['prjid']


        eventdb = getEventDetDB(prjid)
        events, event_dict = eventdb.getEvents()

        ret_code = eventdb.closeConn()
        msg = ''

        if ret_code == 0:
            msg = "success"
        else:
            msg = "failure"

        output = {R_STAT:ret_code, R_MSG:msg, R_EUUID:events, R_DE:event_dict}

        #return status code
        resp.body = json.dumps(output, encoding='utf-8')

        if ret_code == 0:
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_500