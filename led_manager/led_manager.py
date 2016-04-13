#!/bin/python
"""
Uses public backend API to observe access point power states.
Configured RGB-LED bulbs are turned green and red depending on a AP's state.
"""
import logging
import argparse
import os
import sys
from daemon import DaemonBase
import requests
import time
import libledbulbs

API_HOST = "127.0.0.1"
API_PORT = "6680"

AP_LED_MAP = {
    "e60db822c51d330bbf6954f306941678": 1,
    "c3b4a156913a37bf8e11e0bf756fcd9f": 2,
    "dd8a05d9212131dcbb531ffc5cdd3979": 3#,
    #"5bbd409e00fd11e4a3dec8bcc8a0a80d": 4
}


class AP_Request(object):

    def __init__(self):
        pass

    def _get_url(self):
        return "http://%s:%s" % (API_HOST, API_PORT)

    def list(self):
        r = requests.get(self._get_url() + "/api/accesspoint")
        assert(r.status_code == 200)
        return r.json()

    def get(self, url):
        r = requests.get(self._get_url() + url)
        assert(r.status_code == 200)
        return r.json()


class LED_Manager(DaemonBase):  # inherit DaemonBase to build a Unix daemon

    def __init__(self):
        '''
        Constructor
        '''
        super(LED_Manager, self).__init__("/tmp/led_manager.pid")

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
            logfile = "/tmp/led_manager.log"
        # setup logging
        logging.basicConfig(filename=logfile, filemode="w", level=loglevel,
                            format="%(asctime)s [%(levelname)-8s] %(message)s")
        logging.warning("LED Manager logging enabled.")

    def start(self, params, daemonize=True):
        '''
        Runs the server.
        '''
        self.setupLogging(params)
        super(LED_Manager, self).start(params, daemonize)

    def led_init(self):
        libledbulbs.turn_group_on(0)
        time.sleep(1.0)
        libledbulbs.set_group_color(1, "blue")
        time.sleep(0.2)
        libledbulbs.set_group_color(2, "blue")
        time.sleep(0.2)
        libledbulbs.set_group_color(3, "blue")
        time.sleep(0.2)
        libledbulbs.set_group_color(4, "blue")
	time.sleep(0.5)
        libledbulbs.set_group_color(1, "pink")
        time.sleep(0.2)
        libledbulbs.set_group_color(2, "pink")
        time.sleep(0.2)
        libledbulbs.set_group_color(3, "pink")
        time.sleep(0.2)
        libledbulbs.set_group_color(4, "pink")
        time.sleep(1.0)
        libledbulbs.turn_group_off(0)
        time.sleep(1.0)
        libledbulbs.turn_group_on(0)
        time.sleep(0.5)
        libledbulbs.set_group_color(0, "red")

    def run(self, params=None):
        '''
        Sets up the daemon and go into infinity loop.
        '''
        logging.info('LED Manager daemon running with PID: %s'
                     % str(self.pid))
        self.led_init()
        AP = AP_Request()
        apl = None
        while 1:
            try:
                if apl is None:
                    apl = AP.list()
                for url in apl:
                    ap = AP.get(url)
                    led_id = AP_LED_MAP.get(ap["uuid"])
                    color = "blue" if ap["power_state"] == 1 else "green"
                    logging.info("SWITCH led_id:%s color:%s" % (str(led_id), str(color)))
                    if led_id is not None:
                        libledbulbs.set_group_color(led_id, color)
            except:
                logging.exception("Exception in update loop:")
                apl = None
            time.sleep(1.0)


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
    s = LED_Manager()
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
