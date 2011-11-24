__author__ = 'dickon'


import web
import json
import logging
import config

import tuplespaceserver

logging.basicConfig()


urls = (
    '/tuplespace/open', 'openrequest',
    '/tuplespace/check', 'checkrequest',
    '/tuplespace/put', 'putrequest',
    '/tuplespace/take', 'takerequest',
    '/tuplespace/subscribe', 'subscriberequest',
    '/tuplespace/unsubscribe', 'unsubscriberequest',
    '/tuplespace/example', 'examplerequest'
)
app = web.application(urls, globals(), True)

'''class index:
    def GET(self):
        web.seeother('/static/index.html')
'''

class openrequest:

    def __init__(self):
        self.server = tuplespaceserver.server
        self._log = logging.getLogger(name=openrequest.__name__)
        self._log.setLevel(logging.DEBUG)
        self.identity = None

    def GET(self):
        self.identity = web.ctx.env['HTTP_AUTHORIZATION']
        self._log.debug('received GET open from: %s' % self.identity)
        self.server.open(self.identity)
        return 'session open for client: %s' % self.identity

class subscriberequest:

    def __init__(self):
        self.server = tuplespaceserver.server
        self._log = logging.getLogger(name=subscriberequest.__name__)
        self._log.setLevel(logging.DEBUG)
        self.identity = None

    def POST(self):
        self.identity = web.ctx.env['HTTP_AUTHORIZATION']
        self._log.debug('received POST subscribe from: %s' % self.identity)
        payload = web.data()
        self._log.debug('data %s' % payload)
        data = json.loads(payload)
        t = data['tuple']
        self.server.subscribe(self.identity, t)
        return 'subscription set for client: %s' % self.identity

class unsubscriberequest:

    def __init__(self):
        self.server = tuplespaceserver.server
        self._log = logging.getLogger(name=unsubscriberequest.__name__)
        self._log.setLevel(logging.DEBUG)
        self.identity = None

    def POST(self):
        self.identity = web.ctx.env['HTTP_AUTHORIZATION']
        self._log.debug('received POST subscribe from: %s' % self.identity)
        payload = web.data()
        self._log.debug('data %s' % payload)
        data = json.loads(payload)
        t = data['tuple']
        self.server.unsubscribe(self.identity, t)
        return 'subscription removed for client: %s' % self.identity

class putrequest:

    def __init__(self):
        self.server = tuplespaceserver.server
        self._log = logging.getLogger(name=openrequest.__name__)
        self._log.setLevel(logging.DEBUG)
        self.identity = None

    def POST(self):
        self.identity = web.ctx.env['HTTP_AUTHORIZATION']
        self._log.debug('received POST put from: %s' % self.identity)
        payload = web.data()
        self._log.debug('data: %s' % payload)
        data = json.loads(payload)
        t = data['tuple']
        self.server.put(self.identity, t)

class checkrequest:

    def __init__(self):
        self.server = tuplespaceserver.server
        self._log = logging.getLogger(name=checkrequest.__name__)
        self._log.setLevel(logging.DEBUG)
        self.identity = None
    
    def POST(self):
        payload = web.data()
        self.identity = web.ctx.env['HTTP_AUTHORIZATION']
        self._log.debug('received POST check from: %s' % self.identity)
        self._log.debug('data: %s' % payload)
        data = json.loads(payload)
        t = data['tuple']
        # test
        # a = pack(('a', 'b', 'c'))
        # b = pack(('x', 'y', 'z'))
        # tuples = []
         # tuples.append(a)
        # tuples.append(b)
        # end test
        tuples = self.server.check(self.identity, t)
        rdata = {}
        rdata['tuples'] = tuples
        stringified_data = json.dumps(rdata)
        self._log.debug('sending: %s' % stringified_data)
        web.header('Authorization', self.identity)
        web.header('Content-Type', 'application/json')
        return stringified_data

class examplerequest:

    def __init__(self):
        self._log = logging.getLogger(name=examplerequest.__name__)
        self._log.setLevel(logging.DEBUG)

    def GET(self):
        self._log.info('received example request')
        # web.header('Content-Type', 'application/json')
        random_data = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
               "Donec non egestas nisl. Donec quis mauris non sem hendrerit feugiat.",
               "Nulla tempus lacus sed sapien porttitor feugiat. Quisque accumsan viverra sapien.",
               "Duis quis sapien euismod erat bibendum dictum ac vitae turpis. Curabitur scelerisque,",
               "erat id feugiat pulvinar, velit justo aliquam nibh, in ornare neque mi a nulla.",
               "Phasellus tincidunt leo et leo commodo suscipit. Aliquam molestie gravida neque, ",
               "non sagittis justo pulvinar et. Donec mollis ipsum porttitor libero laoreet vitae ",
               "imperdiet risus consectetur. Etiam sem ipsum, porttitor aliquam laoreet vel, laoreet ac ligula.",
               "Vestibulum congue, elit sit amet pulvinar accumsan, odio ipsum congue orci, et volutpat lectus",
               " ante gravida quam. Pellentesque habitant morbi tristique senectus et netus et malesuada fames",
               " ac turpis egestas. Curabitur lobortis tincidunt neque a condimentum. Nam augue urna, ",
               "auctor non bibendum eu, ultrices tristique dolor. Suspendisse ut hendrerit libero. Curabitur",
               " lacinia lacus in justo blandit in tincidunt dolor commodo. Morbi pretium semper est eu congue.")
        rdata = { 'data': random_data }
        stringified_data = json.dumps(rdata)
        self._log.info("response body is: %s" % stringified_data)
        return stringified_data

if __name__ == "__main__":
    app.run()
