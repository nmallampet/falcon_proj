import falcon

from createpm import createpm
from createevent import createevent
from getEvents import getEvents

from falcon.http_status import HTTPStatus

#gunicorn -b 0.0.0.0:5001 pm:api --reload &
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

createpm = createpm()
createevent = createevent()
getevents = getEvents()

api.add_route('/api/v1/createproject', createpm)
api.add_route('/api/v1/createevent', createevent)
api.add_route('/api/v1/getevents', getevents)
