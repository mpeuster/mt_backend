import logging
import math


class BaseAlgorithm(object):

    def __init__(self):
        """
        Initialization work
        """
        pass

    def find_closest_ap(self, ue, ap_list):
        """
        Returns the AP with the minimum distance to the
        given UE. (Helper)
        """

        def distance(ue, ap):
            ue_x = ue["position_x"]
            ue_y = ue["position_y"]
            ap_x = ap["position_x"]
            ap_y = ap["position_y"]
            return math.sqrt(math.pow(abs(ue_x - ap_x), 2)
                             + math.pow(abs(ue_y - ap_y), 2))

        min_distance = float("inf")
        min_ap = None
        for ap in ap_list:
            if distance(ue, ap) < min_distance:
                min_distance = distance(ue, ap)
                min_ap = ap

        logging.debug("[ALGO] Closest AP for UE: %s is: %s"
                      % (ue["device_id"], min_ap["device_id"]))
        return min_ap

    def compute(self, ue_list, ap_list, requesting_ue):
        """
        Computes the assignment of UE to APs and power state for the APs.

        Input:
            - list of UE dicts (structured like REST API return)
            - list of AP dicts (structured like REST API return)
            - uuid of UE which has triggered this algorithm run

        Result:
            Tuple(power_states_dict, assignment_dict)
            - power_states_dict: AP uuid -> power state (True/False)
                e.g. {"ap_uuid": True, "ap_uuid2": False}
            - assignment_dict: UE uuid -> AP uuid / None
                e.g. {"ue_uuid1": "ap_uuid2", "ue_uuid2": None}
        """
        logging.error("Algorithm plugin does not implement compute method.")
        # logging.debug(str(ue_list))
        # logging.debug(str(ap_list))
        # logging.debug(str(requesting_ue))
        # return empty but well formed result
        return ({}, {})
