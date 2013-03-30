'''
Created on 12 May 2011

@author: dickon
'''

import logging
from restclient.transport import HTTPLib2Transport
from restclient.rest import Resource, RestClient
from restclient.errors import RequestFailed, ResourceNotFound, Unauthorized, RequestError
import marshal
import json
import threading

logging.basicConfig()

log = logging.getLogger(name=__name__)
log.setLevel(logging.DEBUG)

class TupleSpace(object):
    '''
    client entry point into the tuple space. A client of the tuple space can:
    1. register interest in tuples that match a tuple
    2. receive notification of tuples that match it
    3. take a tuple from the space
    4. take all matching tuples from the space
    5. add a tuple to the space

    '''

    def __init__(self, serverBaseURI, id, notify_pause=5):
        '''
        serverBaseURI: the http address of the tuple space server
        id: a logical string identifying this client   
        '''
        self._log = logging.getLogger(TupleSpace.__name__)
        self._log.setLevel(logging.DEBUG)
        self._id = id;

        self.registrations = {}
        self.serverProxy = ServerProxy(serverBaseURI, id)
        self.notify_pause = notify_pause

    def open(self):
        self._log.info("opening client with id: %s" % self._id)
        self.serverProxy.open()
        poll(tuplespace_client=self, server_proxy=self.serverProxy)

    def register(self, tuple, listener):
        '''
        Note multiple registrations can be requested through one instance of a TupleSpace client
        '''
        listeners = None
        try:
            listeners = self.registrations[tuple]
        except KeyError:
            listeners = []
            self.registrations[tuple] = listeners

        listeners.append(listener)
        self.serverProxy.subscribe(tuple)
        self._log.info("registration added for %s" % str(tuple))
    
    def unregister(self, tuple, handler):
        pass

    def notify(self, tuple, matches):
        '''
        a call back into the client with matches retrieved
        from a TupleSpace server.
        '''
        listeners = self.registrations[tuple]
        for l in listeners:
            t = threading.Thread(target=l.notify, args=(tuple, matches))
            t.start()

    def take(self, tuple):
        '''
        removes a tuple from the TupleSpace
        '''
        return self.serverProxy.take(tuple)

    def put(self, tuple):
        '''
        adds a tuple to the space
        '''
        return self.serverProxy.put(tuple)

class ServerProxy(object):
    '''
    The ServerProxy encapsulates the actual interaction with the tuple space server
    It provides functions to:
    1. register a client's interest in a tuples that match a tuple
    2. unregister, of course
    3. intermittently poll the tuple space for matches that have occurred
    4. add tuples to the space
    5. remove tuples from the space
    '''

    def __init__(self, serverBaseURI, id):
        self.id = id
        self.serverBaseURI = serverBaseURI
        self._log = logging.getLogger(name=ServerProxy.__name__)
        self._log.setLevel(logging.DEBUG)

    def open(self):
        r = Resource(self.serverBaseURI + '/' + 'open', HTTPLib2Transport())
        result = r.get(headers={'Authorization': self.id})
        if not r.response.status == 200:
            raise Exception('unable to open session on tuplespace')

    def put(self, tuple):
        p = pack(tuple)
        data = {}
        data['tuple'] = p
        stringified_data = json.dumps(data)
        r = Resource(self.serverBaseURI + '/' + 'put', HTTPLib2Transport())
        result = r.post(payload=stringified_data, headers={'Authorization': self.id})
        if not r.response.status == 200:
            raise Exception('put on tuplespace failed: %s' % stringified_data)

    def take(self, tuple):
        pass
    
    def subscribe(self, tuple):
        '''
        sends tuple plus some identifier to the server to register interest in
        any tuples that match this one.
        '''
        p = pack(tuple)
        data = {}
        data['tuple'] = p
        stringified_data = json.dumps(data)
        r = Resource(self.serverBaseURI + '/' + 'subscribe', HTTPLib2Transport())
        result = r.post(payload=stringified_data, headers={'Authorization': self.id})
        if not r.response.status == 200:
            raise Exception('subscribe on tuplespace failed: %s' % stringified_data)

    def unsubscribe(self, tuple):
        '''
        sends tuple plus some identifier to the server to unregister interest in
        any tuples that match this one.
        '''
        p = pack(tuple)
        data = {}
        data['tuple'] = p
        stringified_data = json.dumps(data)
        r = Resource(self.serverBaseURI + '/' + 'unsubscribe', HTTPLib2Transport())
        result = r.post(payload=stringified_data, headers={'Authorization': self.id})
        if not r.response.status == 200:
            raise Exception('unsubscribe on tuplespace failed: %s' % stringified_data)

    def check(self, tuple):
        '''
        This method is called by threads initiated by ServerProxy. Its purpose is to
        poll the tuplespace server to see if any matches have occurred for existing subscriptions.
        Returns a list of tuples. Each list contains matching tuples.
        The result is the payload, which should be a json string,
        may need to set accepts header to application/json
        this will be something like
        ["(\\u0002\\u0000\\u0000\\u0000t\\u0001\\u0000\\u0000\\u00005t\\u0001\\u0000\\u0000\\u00006",
        "(\\u0002\\u0000\\u0000\\u0000t\\u0001\\u0000\\u0000\\u00007t\\u0001\\u0000\\u0000\\u00008"]
        which can be de-jsoned to a list of strings, each of which can then be unmarshaled to
        a tuple
        '''
        r = Resource(self.serverBaseURI + '/' + 'check', HTTPLib2Transport())
        p = pack(tuple)
        data = {'tuple': p}
        stringified_data = json.dumps(data)
        result = r.post(payload=stringified_data,headers={'Content-Type': 'application/json', 'Authorization': self.id, \
                                           'Accepts': 'application/json'})
        rdata = json.loads(result)
        packed_tuples = rdata['tuples']
        tuples = []
        for t in packed_tuples:
            next_tuple = unpack(t)
            tuples.append(next_tuple)
        return tuples


def poll(*args, **kwargs):
    tuplespace_client = kwargs['tuplespace_client']
    server_proxy = kwargs['server_proxy']
    log.debug('polling...')
    _timer = threading.Timer(tuplespace_client.notify_pause, poll, (), {'tuplespace_client': tuplespace_client, \
                                                                        'server_proxy': server_proxy})
    _timer.setDaemon(True)
    _timer.start()
    for t in tuplespace_client.registrations.keys():
        tlist = server_proxy.check(t)
        if len(tlist) > 0:
            log.debug('found matches for %s ' % str(t))
            tuplespace_client.notify(t, tlist)
        else:
            log.debug('no matches for %s ' % str(t))
            
def pack(tuple):
    packed = []
    for e in tuple:
        packed.append(marshal.dumps(e))
    log.debug('packed object: %s' % packed)
    return packed

def unpack(packed):
    result = []
    for s in packed:
        result.append(marshal.loads(s))
    t = tuple(result)
    return t

if __name__ == '__main__':
    proxy = ServerProxy('http://localhost:8080/tuplespace', 'id')
    proxy.check()