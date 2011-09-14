

__author__ = 'dickon'

import tuplespace
e = tuplespace.ServerProxy('http://localhost:8080/tuplespace', '1')
e.open()
e.subscribe(('a', 'b'))
e.put(('a', 'b', 'c'))
e.put(('a', 'b', 'c'))
e.put(('x', 'y', 'z'))
r = e.check(('a', 'b'))
e.unsubscribe(('a', 'b'))
print 'matches: ', r

