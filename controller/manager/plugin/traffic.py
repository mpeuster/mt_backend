import base
import logging
import math
from collections import deque


class TrafficThresholdNearestAp(base.BaseAlgorithm):

    def __init__(self):
        """
        Initialization work
        """
        super(TrafficThresholdNearestAp, self).__init__()
        logging.info("Loaded algorithm: %s" % str(self.__class__.__name__))
        self.ue_traffic_data = {}

        # configuration:
        self.MAVG_WINDOW_SIZE = 10
        self.THRESHOLD = 500  # bytes/s

    def monitor_traffic(self, ue_list):
        """
        Monitor MAVG_WINDOW_SIZE last traffic values reported by the UEs,
        to calculate moving averages for threshold comparison.
        """
        for ue in ue_list:
            uri = ue["uri"]
            # add new UE traffic data list, if not present
            if uri not in self.ue_traffic_data:
                self.ue_traffic_data[uri] = deque([0] * self.MAVG_WINDOW_SIZE)
            # add new value (aggregated total traffic)
            new_bps = (float(ue["rx_total_bytes_per_second"])
                       + float(ue["tx_total_bytes_per_second"]))
            self.ue_traffic_data[uri].append(new_bps)
            # remove oldest
            self.ue_traffic_data[uri].popleft()
            assert(len(self.ue_traffic_data[uri]) == self.MAVG_WINDOW_SIZE)
            logging.info("AVG Traffic for %s: %f byte/s"
                         % (ue["device_id"], self.get_avg_traffic(uri)))

    def get_avg_traffic(self, uri):
        if uri in self.ue_traffic_data:
            return (sum(self.ue_traffic_data[uri])
                    / float(len(self.ue_traffic_data[uri])))
        return -1

    def compute(self, ue_list, ap_list, requesting_ue):
        """
        Activate nearest APs based on network traffic thresholds.
        """
        logging.info("Running %s..." % str(self.__class__.__name__))

        power_states_dict = {}
        assignment_dict = {}

        # monitor network traffic of all UEs
        self.monitor_traffic(ue_list)

        # assign closest AP for each UE which has traffic that is bigger than
        # the predefined threshold value
        for ue in ue_list:
            if self.get_avg_traffic(ue["uri"]) > self.THRESHOLD:
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


class TrafficThresholdNearestApSwitchCooldown(TrafficThresholdNearestAp):

    def compute(self, ue_list, ap_list, requesting_ue):
        COOLDOWN = 20  # AP switch of cooldown (seconds)

        # call original compute method
        p, a = super(self.__class__, self).compute(ue_list,
                                                   ap_list,
                                                   requesting_ue)
        # apply constraints and manipulate result
        p2 = self.apply_switch_off_cooldown(p, COOLDOWN)
        return (p, a)
