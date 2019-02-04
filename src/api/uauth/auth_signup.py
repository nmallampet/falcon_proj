import falcon

from signup import signup
from login import login
from activeprj import gPrj

from falcon.http_status import HTTPStatus

#gunicorn -b 0.0.0.0:5000 auth_signup:api --reload &
class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')

#wsgi_app = api = falcon.API(middleware=[HandleCORS() ])
api = falcon.API(middleware=[HandleCORS() ])

signup = signup()
login = login()
gprj = gPrj()

api.add_route('/api/v1/signup', signup)
api.add_route('/api/v1/login', login)
api.add_route('/api/v1/getAllProj', gprj)