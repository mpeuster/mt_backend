import logging
import time


class ApDriver():

    def __init__(self):
        logging.info("[ApDriver] Dummy driver loaded.")

    def set_mac_lists(self, ap):
        logging.info("[ApDriver] Setting MAC lists for %s" % ap)

    def set_power_state(self, ap):
        logging.info("[ApDriver] Setting power state for %s to: %s"
                     % (ap, ap.power_state))

    def get_power_state(self, ap):
        logging.info("[ApDriver] Getting power state for %s" % ap)

    def get_network_stats(self, ap):
        logging.info("[ApDriver] Getting networks stats for %s" % ap)
        return {"aps": [
                {"name": "vap0",
                 "rxbyte": 1234,
                 "rxpkt": 123,
                 "txbyte": 6789,
                 "txpkt": 678,
                 "timestamp": time.time()
                 }]}
