import falcon
import json 

from signup_db import signupDB
from falcon_cors import CORS


R_STAT = "status"
R_UUID = "usrid"
R_MSG = "message"

class signup:


    def on_options(self, req, res):
        res.status = falcon.HTTP_200
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header('Access-Control-Allow-Methods', 'POST')
        res.set_header('Access-Control-Allow-Headers', 'Content-Type')

    def on_post(self, req, resp):

        #get data
        data = json.loads(req.stream.read().encode('utf-8')) 


        #parse json dict
        print data
        email = data['email']
        fname = data['fname']
        lname = data['lname']
        pword = data['pword']

        print email, fname, lname, pword

        usrid = None

        #create user in database
        userdb = signupDB(email, fname, lname, pword)

        email_code = userdb.checkEmail()


        if email_code == 0:
            usrid, create_usr_code = userdb.createUser()
        else:
            create_usr_code = 1

        close_conn_code = userdb.closeConn()

        ret_code = 1
        if close_conn_code == create_usr_code == 0:
            ret_code = 0
        
        if create_usr_code == 1:
            ret_code = 2

        if ret_code == 0:
            msg = "success"
        elif ret_code == 1:
            msg = "failure"
        else:
            msg = "email exists"

        #dump output
        output = {R_STAT:ret_code, R_UUID:usrid, R_MSG:msg}
        #return status code
        resp.body = json.dumps(output, encoding='utf-8')

        if ret_code == 0:
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_500



