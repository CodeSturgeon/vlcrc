import telnetlib
import re
import logging


class VLCRemote(object):
    def __init__(self, hostname, port, timeout=3):
        self.cnx = telnetlib.Telnet(hostname, port)
        self.log = logging.getLogger('VLCRemote')
        self.timeout = timeout

    def _command(self, cmd, return_re=None, *args):

        cmd_str = '%s %s\n'%(cmd, ' '.join(args))
        self.log.debug('-> Sending\n%s'%cmd_str)
        self.cnx.write(cmd_str)

        cmd_end = '%s: returned '%cmd
        cmd_ret = self.cnx.read_until(cmd_end,self.timeout)
        if not cmd_ret.ends_with(cmd_end):
            err_str = 'Sent: %s'%cmd_str
            err_str += 'Expected: %s\n'%cmd_end
            err_str += 'Got: %s'%cmd_ret
            self.log.warn(err_str)
            return False

        good = '0 (no error)\r\n'
        cmd_fin = self.cnx.read_until('\r\n',3)
        if cmd_fin != good:
            err_str = 'Sent: %s'%cmd_str
            err_str += 'Expected: %s%s'%(cmd_end,good)
            err_str += 'Got: %s%s'%(cmd_ret,cmd_fin)
            self.log.warn(err_str)
            return False

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
        # Clear the queue
        self.cnx.read_lazy()
        self.cnx.write('get_time\n')
        # FIXME - Fragile, coudld be done better with regex
        time = self.cnx.read_until('\r\n',3)
        if time == '':
            print 'BAD TIME'
            return
        gt = int(time)+duration
        self.cnx.write('seek %d\n'%gt)
        self.cnx.read_until('seek: returned 0 (no error)\r\n',3)

    def next(self):
        self._command('next')

