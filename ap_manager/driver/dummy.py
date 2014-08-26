import logging


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
