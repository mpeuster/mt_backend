import base
import logging
import math


class SimpleNearestApAlgorithm(base.BaseAlgorithm):

    def __init__(self):
        """
        Initialization work
        """
        logging.info("Loaded algorithm: %s" % str(self.__class__.__name__))

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
            - list of UE dicts (structured like REST API JSON response)
            - list of AP dicts (structured like REST API JSON response)
            - uuid of UE which has triggered this algorithm run

        Result:
            Tuple(power_states_dict, assignment_dict)
            - power_states_dict: AP uuid -> power state (True/False)
                e.g. {"ap_uuid": True, "ap_uuid2": False}
            - assignment_dict: UE uuid -> AP uuid / None
                e.g. {"ue_uuid1": "ap_uuid2", "ue_uuid2": None}

        What it does:
            This simple algorithm assigns each UE to its closest AP if the
            display_state of the UE != 0.
            All APs which have at least one UE assigned are switched on.
        """
        logging.info("Running %s..." % str(self.__class__.__name__))

        power_states_dict = {}
        assignment_dict = {}

        # assign closest AP for each UE with display_state != 0
        for ue in ue_list:
            if ue["display_state"] != 0:
                closest_ap = self.find_closest_ap(ue, ap_list)
                if closest_ap is not None:
                    assignment_dict[ue["uuid"]] = closest_ap["uuid"]

        # switch on all APs which are assigned to at least on UE
        for ap in ap_list:
            if ap["uuid"] in assignment_dict.itervalues():
                power_states_dict[ap["uuid"]] = True
            else:  # turn off all unassigned APs
                power_states_dict[ap["uuid"]] = False

        # return({}, {})
        return (power_states_dict, assignment_dict)
