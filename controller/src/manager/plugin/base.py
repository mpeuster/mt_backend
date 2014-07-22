import logging


class BaseAlgorithm(object):

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
