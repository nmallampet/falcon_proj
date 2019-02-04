import falcon
import json 

from createpm_db import pmDB


R_STAT = "status"
R_PUUID = "prjid"
R_MSG = "message"

class createpm:


    def on_options(self, req, res):
        res.status = falcon.HTTP_200
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header('Access-Control-Allow-Methods', 'POST')
        res.set_header('Access-Control-Allow-Headers', 'Content-Type')

    def on_post(self, req, resp):

        #get data
        data = json.loads(req.stream.read()) 


        #parse json dict
        prjname = data['prjname']
        usrid = data['usrid']


        print prjname, usrid

        #create pm
        pmdb = pmDB(prjname, usrid)
        prjid = pmdb.createPM()

        ret_code = pmdb.closeConn()

        msg = None
        if ret_code == 0:
            msg = "success"
        else:
            msg = "failure"



        #dump output
        output = {R_STAT:ret_code, R_MSG:msg, R_PUUID:prjid}

        #return status code
        resp.body = json.dumps(output, encoding='utf-8')

        if ret_code == 0:
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_500



