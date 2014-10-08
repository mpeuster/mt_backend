"""
    UPB Access Point Manager

    Copyright (C) 2014 Manuel Peuster <manuel@peuster.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
import argparse
import os
import sys
from daemon import DaemonBase
import api


class UPB_APM(DaemonBase):  # inherit DaemonBase to build a Unix daemon

    def __init__(self):
        '''
        Constructor
        '''
        super(UPB_APM, self).__init__("/tmp/upb_apm.pid")

    def setupLogging(self, params):
        '''
        Logging setup.
        '''
        if params is None:
            raise Exception("Missing arguments for logging setup.")
            return
        if params.loglevel == "debug" or params.verbose:
            loglevel = logging.DEBUG
        elif params.loglevel == "warning":
            loglevel = logging.WARNING
        else:
            loglevel = logging.INFO
        if params.verbose:
            logfile = None
        else:
            logfile = "/tmp/upb_apm.log"
        # setup logging
        logging.basicConfig(filename=logfile, filemode="w", level=loglevel,
                            format="%(asctime)s [%(levelname)-8s] %(message)s")
        logging.warning("UPB-APN API logging enabled.")

    def start(self, params, daemonize=True):
        '''
        Runs the server.
        '''
        self.setupLogging(params)
        super(UPB_APM, self).start(params, daemonize)

    def run(self, params=None):
        '''
        Sets up the daemon and go into infinity loop.
        '''
        logging.info('UPB-APN API daemon running with PID: %s'
                     % str(self.pid))
        # Run API server instance
        apisrv = api.APIServer(params)
        try:
            apisrv.run()
        except:
            logging.exception("Exception in API:")


def parse_arguments():
    '''
    Initializes command line argument parser.
    Sets up logging environment.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", dest="verbose",
                        action="store_true",
                        help="Runs the daemon directly in the shell. Logs are"
                        " printed to screen. Loglevel is always: DEBUG.")
    parser.add_argument("-d", "--dummy", dest="dummy",
                        action="store_true",
                        help="Triggers dummy mode.")
    parser.add_argument("-l", "--loglevel", dest="loglevel",
                        choices=['debug', 'info', 'warning'],
                        help="Defines the used logging level.")
    parser.add_argument("-a", "--action", dest="action",
                        choices=['start', 'stop', 'restart', 'status'],
                        help="Action which should be performed on daemon.")
    parser.add_argument("-c", "--config", dest="config", default="config.json",
                        help="Path to config file. Default: config.json.")
    params = parser.parse_args()
    return params


if __name__ == '__main__':
    # parse command line parameters
    params = parse_arguments()
    params.path = os.path.dirname(os.path.abspath(__file__)) + "/"
    # create daemon instance
    s = UPB_APM()
    # process command
    if params.action == 'start':
        s.start(params, daemonize=not params.verbose)
    elif params.action == 'stop':
        s.stop()
    elif params.action == 'restart':
        s.restart(params, daemonize=not params.verbose)
    elif params.action == 'status':
        pid = s.getPID()
        if pid > 0:
            print "Daemon is running with PID: %d." % pid
        else:
            print "Daemon is not running."
