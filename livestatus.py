import csv
import socket

OP_EQ = '='
OP_MAP = {
    'lt': '<',
    'gt': '>',
    'lte': '<=',
    'gte': '>=',
    'ne': '!=',
}


class Query(object):
    def __init__(self, conn, resource):
        self._conn = conn
        self._resource = resource
        self._columns = []
        self._filters = []

    def call(self):
        if self._columns:
            return self._conn.call(str(self), self._columns)
        return self._conn.call(str(self))

    def __str__(self):
        request = 'GET %s' % (self._resource)
        if self._columns and any(self._columns):
            request += '\nColumns: %s' % (' '.join(self._columns))
        if self._filters:
            request += ''.join(self._filters)
        return request + '\n\n'

    def columns(self, *args):
        self._columns = args
        return self

    def filter(self, **kwargs):
        for key, value in kwargs.iteritems():
            if '__' in key:
                key, op = key.split('__')
                op = OP_MAP.get(op, OP_EQ)
            else:
                op = OP_EQ
            self._filters.append(
                '\nFilter: {} {} {}'.format(key, op, value)
            )
        return self


class Socket(object):
    def __init__(self, peer):
        self.peer = peer

    def __getattr__(self, name):
        return Query(self, name)

    def call(self, request, columns=None):
        try:
            if len(self.peer) == 2:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(self.peer)
            s.send(request)
            s.shutdown(socket.SHUT_WR)
            csv_lines = csv.DictReader(s.makefile(), columns, delimiter=';')
            return list(csv_lines)
        finally:
            s.close()
