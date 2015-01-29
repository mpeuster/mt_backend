#!/bin/python
"""
Uses public backend API to observe access point power states.
Configured RGB-LED bulbs are turned green and red depending on a AP's state.
"""
import requests
import time
import libledbulbs

API_HOST = "127.0.0.1"
API_PORT = "6680"

AP_LED_MAP = {
    "9d7034c5008b11e4b714c8bcc8a0a80d": 1,
    "5e8e61d100fd11e4bfafc8bcc8a0a80d": 2,
    "57ae409e00fd11e4a3dec8bcc8a0a80d": 3,
    "5bbd409e00fd11e4a3dec8bcc8a0a80d": 4
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


def init():
    libledbulbs.turn_group_on(0)
    time.sleep(1.0)
    libledbulbs.set_group_color(1, "blue")
    time.sleep(0.5)
    libledbulbs.set_group_color(2, "blue")
    time.sleep(0.5)
    libledbulbs.set_group_color(3, "blue")
    time.sleep(0.5)
    libledbulbs.set_group_color(4, "blue")
    time.sleep(1.0)
    libledbulbs.turn_group_off(0)
    time.sleep(1.0)
    libledbulbs.turn_group_on(0)
    time.sleep(0.5)
    libledbulbs.set_group_color(0, "red")


def run():
    AP = AP_Request()
    apl = AP.list()
    while 1:
        for url in apl:
            ap = AP.get(url)
            led_id = AP_LED_MAP.get(ap["uuid"])
            color = "green" if ap["power_state"] == 1 else "red"
            if led_id is not None:
                libledbulbs.set_group_color(led_id, color)
        time.sleep(1.0)


def main():
    init()
    run()

if __name__ == '__main__':
    main()
