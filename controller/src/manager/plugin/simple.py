import base
import logging


class SimpleNearestApAlgorithm(base.BaseAlgorithm):

    def __init__(self):
        """
        Initialization work
        """
        logging.info("Loaded algorithm: %s" % str(self.__class__.__name__))

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
        """
        # TODO: Implement real algorithm
        logging.info("Running %s..." % str(self.__class__.__name__))

        power_states_dict = {}
        assignment_dict = {}

        # switch on all APs
        for ap in ap_list:
            power_states_dict[ap["uuid"]] = True

        # assign ap1 to all UE
        for ue in ue_list:
            if len(ap_list) > 0:
                assignment_dict[ue["uuid"]] = ap_list[0]["uuid"]

        # return({}, {})
        return (power_states_dict, assignment_dict)
