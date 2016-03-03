import base
import logging
import math

# this threshold must be exceeded when the distance
# from a single UE to two APs is nearly the same
DISTANCE_THRESHOLD = 2


class SimpleNearestAp(base.BaseAlgorithm):
    """
    This simple algorithm assigns each UE to its closest AP if the
    display_state of the UE != 0.
    All APs which have at least one UE assigned are switched on.
    """

    def __init__(self):
        """
        Initialization work
        """
        super(SimpleNearestAp, self).__init__()
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
        logging.info("Running %s..." % str(self.__class__.__name__))

        power_states_dict = {}
        assignment_dict = {}

        # assign closest AP for each UE with display_state != 0
        for ue in ue_list:
            if ue["display_state"] != 0:
                closest_ap = self.find_closest_ap(ue, ap_list,
                                                  threshold=DISTANCE_THRESHOLD)
                if closest_ap is not None:
                    assignment_dict[ue["uuid"]] = closest_ap["uuid"]

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


class SimpleNearestApSwitchCooldown(SimpleNearestAp):

    def compute(self, ue_list, ap_list, requesting_ue):
        COOLDOWN = 20  # AP switch of cooldown (seconds)

        # call original compute method
        p, a = super(self.__class__, self).compute(ue_list,
                                                   ap_list,
                                                   requesting_ue)
        # apply constraints and manipulate result
        p2 = self.apply_switch_off_cooldown(p, COOLDOWN)
        return (p2, a)
