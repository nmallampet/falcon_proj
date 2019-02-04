import falcon
import json 

from falcon_cors import CORS
from activeprj_db import aprjDB

R_APRJ = "active_prj"
R_IPRJ = "inactive_prj"
R_STAT = "status"
R_MSG = "message"
R_DAPRJ = "details_active_prj"
R_DIPRJ = "details_inactive_prj"


class gPrj():
	'''
		CORS header
	'''
    def on_options(self, req, res):
        res.status = falcon.HTTP_200
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header('Access-Control-Allow-Methods', 'POST')
        res.set_header('Access-Control-Allow-Headers', 'Content-Type')
    
    
	'''
		on post call, get userid as input and return proj details as json
	'''
    def on_post(self, req, resp):
        data = json.loads(req.stream.read())

        usrid = data['usrid']

        print usrid

        prjDB = aprjDB(usrid)

        aprj, iprj, msg, aprj_dict, iprj_dict = prjDB.getPrjs()

        ret_code = prjDB.closeConn()

        #dump output
        output = {R_STAT:ret_code, R_MSG:msg, R_APRJ:aprj, R_IPRJ:iprj, R_DAPRJ:aprj_dict, R_DIPRJ:iprj_dict}

        resp.body = json.dumps(output, encoding='utf-8')
        
        if ret_code == 0:
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_500
