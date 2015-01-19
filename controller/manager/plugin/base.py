import logging
import math
import time


class BaseAlgorithm(object):

    def __init__(self):
        """
        Initialization work
        """
        self.ap_switch_on_timestamps = {}
        self.last_assignment = {}

    @property
    def name(self):
        return self.__class__.__name__

    def distance(self, ue, ap):
        ue_x = ue["position_x"]
        ue_y = ue["position_y"]
        ap_x = ap["position_x"]
        ap_y = ap["position_y"]
        return math.sqrt(math.pow(abs(ue_x - ap_x), 2)
                         + math.pow(abs(ue_y - ap_y), 2))

    def find_closest_ap(self, ue, ap_list, threshold=0):
        """
        Helper:
        Returns the AP with the minimum distance to the
        given UE.
        Threshold in distance units which has to be exceeded to
        switch to the next AP.
        """
        min_distance = float("inf")
        min_ap = None
        for ap in ap_list:
            if self.distance(ue, ap) < min_distance:
                min_distance = self.distance(ue, ap)
                min_ap = ap

        logging.debug("[ALGO] Closest AP for UE: %s is: %s"
                      % (ue["device_id"], min_ap["device_id"]))

        # check for switch threshold between old and new closest AP
        if threshold > 0:
            last_ap = self.get_ap(self.last_assignment.get(ue["uuid"]),
                                  ap_list)
            if last_ap is not None:
                logging.info("Checking for threshold with last AP: %s"
                             % str(last_ap.get("uri")))
                if (self.distance(ue, min_ap) + threshold
                        >= self.distance(ue, last_ap)):
                    # threshold not yet exceeded, keep old AP
                    logging.info("Threshold not exceeded. Keeping old AP.")
                    return last_ap
                else:
                    logging.info("Threshold exceeded using new closest AP.")
        return min_ap

    def find_farthest_ue(self, ap, ue_list):
        """
        Helper:
        Returns the UE with the maximum distance to the
        given AP.
        """
        max_distance = -1.0
        max_ue = None
        for ue_uri in ap["assigned_ue_list"]:
            ue = self.get_ue(ue_uri, ue_list)
            if ue is None:
                continue
            if self.distance(ue, ap) > max_distance:
                max_distance = self.distance(ue, ap)
                max_ue = ue
        return max_ue

    def get_ue(self, uri, ue_list):
        for ue in ue_list:
            if uri == ue.get("uri"):
                return ue
            if uri == ue.get("uuid"):
                return ue
            return None

    def get_ap(self, uri, ap_list):
        for ap in ap_list:
            if uri == ap.get("uri"):
                return ap
            if uri == ap.get("uuid"):
                return ap
            return None

    def apply_switch_off_cooldown(self, power_states_dict, cooldown=30):
        """
        Helper
        Only switches of an access point if it was already switched on
        for at least the defined cooldown time.

        Timestamps dict: uuid -> ts (-1 = not switched on yet)
        """
        for uuid in power_states_dict:
            if uuid not in self.ap_switch_on_timestamps:
                self.ap_switch_on_timestamps[uuid] = -1
            if power_states_dict[uuid]:
                # AP should be switched on
                # update switch on timestamps
                self.ap_switch_on_timestamps[uuid] = time.time()
            else:
                # AP should be switched off
                if self.ap_switch_on_timestamps[uuid] > 0:
                    # AP is currently on, test if switch of is ok?
                    if (abs(time.time() - self.ap_switch_on_timestamps[uuid])
                            > cooldown):
                        # switch off action is ok, reset timestamp
                        self.ap_switch_on_timestamps[uuid] = -1
                    else:
                        # switch off action is too early, abort switch action
                        power_states_dict[uuid] = True
                        logging.info("Switch off canceled for %s cooldown: %f"
                                     % (uuid, abs(time.time()
                                        - self.ap_switch_on_timestamps[uuid])))
        return power_states_dict

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
