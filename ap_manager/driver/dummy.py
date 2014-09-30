import logging
import time
import random


class ApDriver():

    def __init__(self):
        logging.info("[ApDriver] Dummy driver loaded.")
        self.rxbyte1 = 0
        self.txbyte1 = 0
        self.rxbyte2 = 0
        self.txbyte2 = 0

    def set_mac_lists(self, ap):
        logging.info("[ApDriver] Setting MAC lists for %s" % ap)

    def set_power_state(self, ap):
        logging.info("[ApDriver] Setting power state for %s to: %s"
                     % (ap, ap.power_state))

    def get_power_state(self, ap):
        logging.info("[ApDriver] Getting power state for %s" % ap)

    def get_network_stats(self, ap):
        logging.info("[ApDriver] Getting networks stats for %s" % ap)
        # use random values for network stats in dummy driver
        # (helps for testing client applications)
        self.rxbyte1 += random.uniform(0, 10000)
        self.txbyte1 += random.uniform(0, 10000)
        self.rxbyte2 += random.uniform(0, 10000)
        self.txbyte2 += random.uniform(0, 10000)
        # also use 2 network interfaces to cover the case of multiple
        # interfaces per access point (e.g. MobiMesh)
        return {"aps": [
                {"name": "vap0",
                 "rxbyte": self.rxbyte1,
                 "rxpkt": 0,
                 "txbyte": self.txbyte1,
                 "txpkt": 0,
                 "timestamp": time.time()
                 },
                {"name": "vap1",
                 "rxbyte": self.rxbyte2,
                 "rxpkt": 0,
                 "txbyte": self.txbyte2,
                 "txpkt": 0,
                 "timestamp": time.time()
                 }]}
