import sys
import os
import time
import atexit
from signal import SIGTERM


class DaemonBase(object):
    '''
    Base class for creating an UNIX daemon process.
    '''

    def __init__(self, pidfile,
                 stdin=os.devnull, stdout=os.devnull, stderr=os.devnull):
        '''
        Init input values
        '''
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.pid = None

    def fork_process(self):
        """
        Fork two times to create a real UNIX daemon with IO to /dev/null
        """
        try:
            pid = os.fork()  # first fork
            if pid > 0:
                sys.exit(0)  # exit parent
        except OSError, e:
            sys.stderr.write("fork failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        # set base environment
        base_path = os.path.split(sys.argv[0])[0] + "/"
        os.chdir(base_path)
        os.setsid()
        os.umask(0)
        try:
            pid = os.fork()  # second fork
            if pid > 0:
                sys.exit(0)  # exit parent
        except OSError, e:
            sys.stderr.write("fork failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        # create pidfile
        atexit.register(self.delpid)
        atexit.register(self.shutdownlogger)
        pid = str(os.getpid())
        self.pid = pid
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        '''
        Deletes the pid file.
        '''
        os.remove(self.pidfile)

    def shutdownlogger(self):
        '''
        Shuts the logger down.
        '''
        logging.shutdown()

    def start(self, params=None, daemonize=True):
        """
        Start the daemon
        """
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if pid:
            sys.stderr.write("Start failed. Daemon is already running?\n")
            sys.exit(1)
        # Start the daemon
        print "Starting daemon..."
        if daemonize:
            self.fork_process()
        self.run(params)

    def stop(self):
        """
        Stop the daemon
        """
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if not pid:
            sys.stderr.write("Stop failed. Daemon not running?\n")
            return
        # kill daemon process
        print "Stopping daemon..."
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self, params=None, daemonize=True):
        """
        Restart the daemon
        """
        self.stop()
        self.start(params, daemonize)

    def getPID(self):
        """
        Return the daemon's process id (it's pid or -1)
        """
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            return -1
        return pid

    def run(self, params=None):
        """
        Override this method
        """
        pass
