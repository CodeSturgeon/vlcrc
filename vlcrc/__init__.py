import telnetlib
import re
import logging


class VLCRemote(object):
    def __init__(self, hostname, port, timeout=3):
        self.cnx = telnetlib.Telnet(hostname, port)
        self.log = logging.getLogger('VLCRemote')
        self.timeout = timeout

    def _command(self, cmd, return_re=None, raw=False, *args):

        cached = self.cnx.read_eager()
        if cached != '':
            self.log.debug('<- Recived: %s'%cached.strip())

        cmd_str = '%s %s\n'%(cmd, ' '.join(args))
        self.log.debug('-> Sending: %s'%cmd_str.strip())
        self.cnx.write(cmd_str)

        if not raw:
            cmd_end = '%s: returned '%cmd
            cmd_ret = self.cnx.read_until(cmd_end,self.timeout)
            if not cmd_ret.endswith(cmd_end):
                err_str = 'Sent: %s'%cmd_str
                err_str += 'Expected: %s\n'%cmd_end
                err_str += 'Got: %s'%cmd_ret
                self.log.warn(err_str)
                return False

            good = '0 (no error)\r\n'
            cmd_fin = self.cnx.read_until('\r\n',3)
            cmd_ret += cmd_fin
            if cmd_fin != good:
                err_str = 'Sent: %s'%cmd_str
                err_str += 'Expected: %s%s'%(cmd_end,good)
                err_str += 'Got: %s'%(cmd_ret)
                self.log.warn(err_str)
                return False
            self.log.debug('<- Recived: %s'%cmd_ret.strip())
        else:
            print return_re
            index, match, cmd_ret = self.cnx.expect([return_re], self.timeout)
            if match is None:
                return False
            self.log.debug('<- Recived: %s'%cmd_ret.strip())
            return match

        if return_re is None:
            return True

        match = return_re.search(''.join((cmd_ret,cmd_fin)))
        return match

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
        #time_re = re.compile('^(?:<time>d+)\r\n')
        time_re = re.compile('(?:<time>\d+)\r\n')
        ret = self._command('get_time', time_re, raw=True)
        if ret:
            time = ret.group_dict()['time']
            gt = int(time)+duration
            self.cnx.write('seek %d\n'%gt)
            self.cnx.read_until('seek: returned 0 (no error)\r\n',3)

    def next(self):
        self._command('next')
