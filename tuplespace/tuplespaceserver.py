__author__ = 'dickon'

import logging
import threading
import marshal

none_value = marshal.dumps(None)

def is_match(tuple1, tuple2):
    i = -1
    match = True
    if len(tuple1) == 0 or len(tuple2) == 0: return False
    for e in tuple1:
        i = i+1
        if i > (len(tuple2)-1):
            break
        if e == none_value:
            continue
        if not e == tuple2[i]:
            match = False
    return match

class TupleSpaceServer(object):
    '''
    In general a TupleSpaceServer simply acts as an endpoint for the request, the matching process is done by another component
    that in most cases will be a daemon process.
    TupleSpaceServer does the following:

    1. For Put requests adds an instance of a Tuple to the space. This always succeeds
    2. For Take requests synchronously removes and returns matching Tuples
    3. For subscriptions, polls the subscription output queue for responses to clients
    4. For subscriptions, registers a new subscription for matching Tuples
    '''
    def open(self, id):
        raise NotImplementedError
    def close(self, id):
        raise NotImplementedError
    def check(self, id, tuple):
        raise NotImplementedError
    def put(self, id, tuple):
        '''
        Put should not fail - create a Put request on the input queue for the space
        and then return. Processing of the Put will occur asynchronously some time
        after the Put has been accepted.
        This means that the precise state of the space will not strictly conform to the
        precise timing of the Put requests, but it will be consistent with their order, which
        is what matters
        '''
        raise NotImplementedError
    def take(self, id, tuple):
        raise NotImplementedError
    def subscribe(self, id, tuple):
        raise NotImplementedError
    def unsubscribe(self, id, tuple):
        raise NotImplementedError

class MongoDBTupleSpaceServer(TupleSpaceServer):
    '''
    TODO: This is the next target to implement. Since the packed form of the tuples can easily be
    represented as a JSON string it seems there may be potential to benefit from MongoDBs scalable
    storage and query facilities for JS objects.
    '''
    pass

class TestTupleSpaceServer(TupleSpaceServer):
    '''
    TestTupleSpaceServer is a very simple in-memory implementation of a TupleSpaceServer
    '''

    none_value = marshal.dumps(None)
    
    def __init__(self):
        self._log = logging.getLogger(TestTupleSpaceServer.__name__)
        self._log.setLevel(logging.DEBUG)
        self._clients = {}
        self._tuples = []
        self._lock = threading.RLock()

    def open(self, id):
        '''
        For this implementation simply creates the dict that will hold the subscriptions (tuples indexing lists of lists)
        for the client with id 'id'
        '''
        self._lock.acquire()
        try:
            subscriptions = self._clients[id]
        except KeyError:
            subscriptions = {}
            self._clients[id] = subscriptions
        self._lock.release()

    def close(self, id):
        pass

    def check(self, id, t):
        '''
        This is a polling request to see if any matches have occurred. Checks an
        internal dictionary of queues (keyed by 'tuple') owned by this id for matches for the tuple 'tuple'
        '''
        self._lock.acquire()
        real_tuple = tuple(t)
        subscriptions = self._clients[id]
        result = []
        try:
            matches = subscriptions[real_tuple]
            if len(matches) > 0:
                for t in matches:
                    list_form = list(t)
                    result.append(list_form)
                # now remove matches since they will be notified to client
                subscriptions[real_tuple] = []
        except KeyError:
            pass
        self._lock.release()
        return result

    def put(self, id, t):
        '''
        This tuple space allows duplicate tuples. Parties wishing to ensure that their
        tuples remain discrete should use a unique identifier as part of the tuple
        '''
        self._lock.acquire()
        real_tuple = tuple(t)
        self._tuples.append(real_tuple)
        for clientid in self._clients.keys():
            subscriptions = self._clients[clientid]
            for sub in subscriptions.keys():
                if is_match (sub, real_tuple):
                    matches = subscriptions[sub]
                    matches.append(real_tuple)
        self._lock.release()

    def take(self, id, t):
        self._lock.acquire()
        real_tuple = tuple(t)
        self._tuples.remove(real_tuple)
        for clientid in self._clients.keys():
            subscriptions = self._clients[clientid]
            for sub in subscriptions.keys():
                matches = subscriptions[sub]
                matches.remove(real_tuple)
        self._lock.release()

    def subscribe(self, id, t):
        self._lock.acquire()
        real_tuple = tuple(t)
        subscriptions = None
        try:
            subscriptions = self._clients[id]
        except KeyError:
            subscriptions = {}
            self._clients[id] = subscriptions
        matches = None
        try:
            matches = subscriptions[real_tuple]
            raise AlreadySubscribedException(real_tuple)
        except KeyError:
            matches = []
            subscriptions[real_tuple] = matches
            for t1 in self._tuples:
                if is_match(t, t1):
                    matches.append(t1)
        self._lock.release()

    def unsubscribe(self, id, t):
        self._lock.acquire()
        real_tuple = tuple(t)
        subscriptions = self._clients[id]
        try:
            matches = subscriptions[real_tuple]
            del subscriptions[real_tuple]
        except KeyError:
            raise NoSuchSubscriptionException(real_tuple)
        self._lock.release()


class AlreadySubscribedException(Exception):
    def __init__(self, tuple):
        self.tuple = tuple

class NoSuchSubscriptionException(Exception):
    def __init__(self, tuple):
        self.tuple = tuple

server = TestTupleSpaceServer()
