import logging


class BaseAlgorithm(object):
    pass

    def compute(self, ue_list, ap_list, requesting_ue):
        # TODO: return a empty but correct result (add a test?)
        logging.error("Algorithm plugin does not implement compute method.")
        # logging.debug(str(ue_list))
        # logging.debug(str(ap_list))
        logging.debug(str(requesting_ue))
