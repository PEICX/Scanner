# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/31 15:58'

import threading

class Node(object):
    __slots__ = ['prev', 'next', 'me']

    def __init__(self, prev, me):
        self.prev = prev
        self.me = me
        self.next = None


class LRU:
    """
    Implementation of a length-limited O(1) LRU queue.
    Built for and used by PyPE:
    http://pype.sourceforge.net
    Copyright 2003 Josiah Carlson.

    These is a list of the modifications that I (Andres Riancho) introduced to the code:
        - Thread safety

    >>> lru_test = LRU(4)
    >>> lru_test['1'] = 1
    >>> lru_test['2'] = 1
    >>> lru_test['3'] = 1
    >>> lru_test['4'] = 1

    # Adding one more, the '1' should go away
    >>> lru_test['5'] = 1
    >>> '1' in lru_test
    False
    >>> '5' in lru_test
    True
    """

    def __init__(self, count, pairs=[]):
        self.lock = threading.RLock()
        self.count = max(count, 1)
        self.d = {}
        self.first = None
        self.last = None
        for key, value in pairs:
            self[key] = value

    def __contains__(self, obj):
        return obj in self.d

    def __getitem__(self, obj):
        with self.lock:
            item = self.d[obj].me
            self[item[0]] = item[1]
            return item[1]

    def __setitem__(self, obj, val):
        with self.lock:
            if obj in self.d:
                del self[obj]
            nobj = Node(self.last, (obj, val))
            if self.first is None:
                self.first = nobj
            if self.last:
                self.last.next = nobj
            self.last = nobj
            self.d[obj] = nobj
            if len(self.d) > self.count:
                if self.first == self.last:
                    self.first = None
                    self.last = None
                    return
                item = self.first
                item.next.prev = None
                self.first = item.next
                item.next = None
                del self.d[item.me[0]]
                del item

    def __delitem__(self, obj):
        with self.lock:
            nobj = self.d[obj]
            if nobj.prev:
                nobj.prev.next = nobj.next
            else:
                self.first = nobj.next
            if nobj.next:
                nobj.next.prev = nobj.prev
            else:
                self.last = nobj.prev
            del self.d[obj]

    def __iter__(self):
        cur = self.first
        while cur is not None:
            cur2 = cur.next
            yield cur.me[1]
            cur = cur2

    def iteritems(self):
        cur = self.first
        while cur is not None:
            cur2 = cur.next
            yield cur.me
            cur = cur2

    def iterkeys(self):
        return iter(self.d)

    def itervalues(self):
        for i, j in self.iteritems():
            yield j

    def keys(self):
        return self.d.keys()

    def __len__(self):
        return len(self.d)

    def values(self):
        return [i.me[1] for i in self.d.values()]