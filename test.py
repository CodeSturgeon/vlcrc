#!/usr/bin/env python
import telnetlib
import re
from easygui import multenterbox, buttonbox, codebox
import pprint

class VLCRemote(object):
    def __init__(self, hostname, port):
        self.cnx = telnetlib.Telnet(hostname, port)

    def get_filename(self):
        # Clear the queue
        self.cnx.read_lazy()
        self.cnx.write('status\n')
        status = self.cnx.read_until('status: returned 0 (no error)\r\n',3)
        match = re.search('input: (.+?) \)',status,re.MULTILINE)
        if match is None:
            print 'BAD STATUS'
            print status
        else:
            return match.group(1)[7:]

    def restart(self):
        self.cnx.write('seek 0\n')
        self.cnx.read_until('seek: returned 0 (no error)\r\n',3)

    def skip(self, duration=60):
        self.cnx.write('get_time\n')
        time = self.cnx.read_until('\r\n',3)
        if time == '':
            print 'BAD TIME'
            return
        gt = int(time)+duration
        self.cnx.write('seek %d\n'%gt)
        self.cnx.read_until('seek: returned 0 (no error)\r\n',3)

    def next(self):
        self.cnx.write('next\n')
        self.cnx.read_until('seek: returned 0 (no error)\r\n',3)

if 0:
    groups = multenterbox(msg='Enter groups you would like to file to',
                            title='Enter Groups', fields=(1,2,3,4,5),
                            values=('yes','no','maybe','other'))
    groups = filter(None,groups)
else:
    groups=('yes','no','maybe','other')

vlc = VLCRemote('localhost', 4222)
groups_dict = {}

def get_group():
    choice = buttonbox(msg='Assign a group', title='Assign a group',
                        choices=groups)
    fn = vlc.get_filename()
    groups_dict[fn] = choice

while 1:
    menu_selection = buttonbox(title='Menu',choices=(
                                'Next','Set Group','Jump','Quit'))
    if menu_selection == 'Next':
        vlc.next()
    elif menu_selection == 'Set Group':
        get_group()
    elif menu_selection == 'Jump':
        vlc.skip()
    else:
        break

reorg = {}
for fname in groups_dict:
    l = reorg.get(groups_dict[fname],[])
    l.append(fname)
    reorg[groups_dict[fname]] = l

print reorg

str = ''
for grp in reorg:
    str += '--%s\n'%grp
    for fname in reorg[grp]:
        str += '%s\n'%fname


#pp = pprint.PrettyPrinter()
#codebox(msg=pp.pformat(str))
#pp.pprint(str)
print str
