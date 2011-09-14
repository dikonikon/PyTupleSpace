__author__ = 'dickon'

import tuplespace

class Client(object):
    def notify(self, t, m):
        print 'matches for tuple: ', t
        for match in m:
            print match

e = tuplespace.TupleSpace('http://localhost:8080/tuplespace', '1', notify_pause=5)
e1 = tuplespace.TupleSpace('http://localhost:8080/tuplespace', '2', notify_pause=5)
e.open()
e1.open()
e.register(('a', 'b'), Client())
e1.put(('a', 'b', 'c'))

s = raw_input('press any key to finish')
  