mk-livestatus
=============
A modified version of [python-mk-livestatus](https://github.com/arthru/python-mk-livestatus).

## Usage
``` python
>>> from livestatus import Socket
>>> s = Socket("/var/lib/icinga/rw/live")
>>> q = s.hosts.columns('name', 'groups').filter(name='localhost', state=0)
>>> print q
GET hosts
Columns: name groups
Filter: name = localhost
Filter: state = 0


>>> q = s.services.columns('host_name', 'contacts').filter(contacts__gte='harri')
>>> print q
GET services
Columns: host_name contacts
Filter: contacts >= harri
