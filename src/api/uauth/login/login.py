import falcon
import json 

from falcon_cors import CORS
from login_db import loginDB


R_STAT = "status"
R_UUID = "usrid"
R_FNAME = "fname"
R_LNAME = "lname"


class login:

    
    def on_options(self, req, res):
        res.status = falcon.HTTP_200
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header('Access-Control-Allow-Methods', 'POST')
        res.set_header('Access-Control-Allow-Headers', 'Content-Type')
    
    

    def on_post(self, req, resp):

        #cors = CORS(allow_origins_list=['http://206.189.169.138:5000'])
        #api = falcon.API(middleware=[cors.middleware])
        #public_cors = CORS(allow_all_origins=True)

        #enable cors
        #cors = public_cors

        #get data
        data = json.loads(req.stream.read()) 


        #parse json dict
        email = data['email']
        pword = data['pword']

        #authenticate in db
        userdb = loginDB(email, pword)
        correctPass, usrid, fname, lname = userdb.confirmUser()
        close_conn_code = userdb.closeConn()

        print email, pword

        
        ret_code = 0

        if not correctPass:
            ret_code = 1

        #dump output
        output = {R_STAT:ret_code, R_UUID:usrid, R_FNAME:fname, R_LNAME:lname}

        #return status code
        resp.body = json.dumps(output, encoding='utf-8')
        
        if ret_code == 0:
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_500



