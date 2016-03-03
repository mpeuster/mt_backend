import base
import logging
import math

# this threshold must be exceeded when the distance
# from a single UE to two APs is nearly the same
DISTANCE_THRESHOLD = 5


class GreedyMinActiveApsFullCoverage(base.BaseAlgorithm):
    """
    Greedy assign UEs to APs which have the most UEs in their
    coverage area.
    It is possible that UEs are not assigned if they are out
    of coverage.
    """

    def __init__(self):
        """
        Initialization work
        """
        super(GreedyMinActiveApsFullCoverage, self).__init__()
        logging.info("Loaded algorithm: %s" % str(self.__class__.__name__))
        self.coverage_ranges = {
            "green01": 15,
            "green02": 15,
            "green03": 15,
            "green04": 15,
            "green05": 15
        }

    def get_ap_range(self, ap_name):
        if ap_name not in self.coverage_ranges:
            logging.error("AP coverage not found: %s" % ap_name)
        return self.coverage_ranges.get(ap_name)

    def get_ues_covered_by_ap(self, ap, ue_list):
        """
        Returns list of UEs that are in the coverage area of
        the given AP. List can be empty.
        """
        result = []
        ap_range = self.get_ap_range(ap.get("device_id"))
        if ap_range is None:
            return []
        for ue in ue_list:
            if self.distance(ue, ap) <= ap_range:
                result.append(ue)
        logging.info("AP: %s coverage: %s",
                     ap.get("device_id"),
                     [ue.get("device_id") for ue in result])
        return result

    def get_ap_with_most_covered_ues(self, ap_list, ue_list):
        """
        Find the AP that covers most of the give UEs.
        Return tuple: AP object and the list of covered UEs.
        """
        best_ap = None
        best_ap_ue_list = []
        for ap in ap_list:
            tmp = self.get_ues_covered_by_ap(ap, ue_list)
            if len(tmp) > len(best_ap_ue_list):
                best_ap_ue_list = list(tmp)
                best_ap = ap
        if best_ap is not None:
            logging.info("Best AP: %s with: %s",
                         best_ap.get("device_id"),
                         [ue.get("device_id") for ue in best_ap_ue_list])
        return (best_ap, best_ap_ue_list)

    def remove_ue_from_list(self, ue_list, remove_ue):
        if remove_ue is None:
            return ue_list
        return [ue for ue in ue_list
                if ue.get("uuid") != remove_ue.get("uuid")]

    def compute(self, ue_list, ap_list, requesting_ue):
        logging.info("Running %s..." % str(self.__class__.__name__))

        power_states_dict = {}
        assignment_dict = {}

        active_ues_to_be_assigned = [ue for ue in ue_list
                                     if ue.get("display_state") != 0]

        # greedy assign UEs to APs with best coverage
        tries = 0
        while(len(active_ues_to_be_assigned) > 0 and tries < len(ap_list)):
            logging.info("UEs TODO: %s",
                         [ue.get("device_id")
                          for ue in active_ues_to_be_assigned])
            ap, ues = self.get_ap_with_most_covered_ues(
                ap_list, active_ues_to_be_assigned)
            if ap is not None:
                for ue in ues:
                    # assign UE to AP
                    assignment_dict[ue["uuid"]] = ap["uuid"]
                    # remove the assigned UE from todo list
                    active_ues_to_be_assigned = self.remove_ue_from_list(
                        active_ues_to_be_assigned, ue)
            tries += 1

        # switch on all APs which are assigned to at least on UE
        for ap in ap_list:
            if ap["uuid"] in assignment_dict.itervalues():
                power_states_dict[ap["uuid"]] = True
            else:  # turn off all unassigned APs
                power_states_dict[ap["uuid"]] = False
        # store this assignment for the next run
        self.last_assignment = assignment_dict.copy()
        # return({}, {})
        return (power_states_dict, assignment_dict)
