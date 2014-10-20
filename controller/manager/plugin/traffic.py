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
        self.THRESHOLD = 10000  # bytes/s

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


class ApTrafficThresholdNearestAp(base.BaseAlgorithm):

    def __init__(self):
        """
        Initialization work
        """
        super(ApTrafficThresholdNearestAp, self).__init__()
        logging.info("Loaded algorithm: %s" % str(self.__class__.__name__))
        self.ap_traffic_data = {}

        # configuration:
        self.MAVG_WINDOW_SIZE = 10
        self.THRESHOLD = 10000  # bytes/s

    def monitor_traffic(self, ap_list):
        """
        Monitor MAVG_WINDOW_SIZE last traffic values reported by the APs,
        to calculate moving averages for threshold comparison.
        """
        for ap in ap_list:
            uri = ap["uri"]
            # add new AP traffic empty data entry to dict, if not present
            if uri not in self.ap_traffic_data:
                self.ap_traffic_data[uri] = deque([0] * self.MAVG_WINDOW_SIZE)
            # add new value (aggregated total traffic)
            new_bps = (float(ap["rx_bytes_per_second"])
                       + float(ap["tx_bytes_per_second"]))
            self.ap_traffic_data[uri].append(new_bps)
            # remove oldest
            self.ap_traffic_data[uri].popleft()
            assert(len(self.ap_traffic_data[uri]) == self.MAVG_WINDOW_SIZE)
            logging.info("AVG Traffic for %s: %f byte/s"
                         % (ap["device_id"], self.get_avg_traffic(uri)))

    def get_avg_traffic(self, uri):
        if uri in self.ap_traffic_data:
            return (sum(self.ap_traffic_data[uri])
                    / float(len(self.ap_traffic_data[uri])))
        return -1

    def compute(self, ue_list, ap_list, requesting_ue):
        """
        Activate nearest APs based on network traffic thresholds,
        measured on APs.
        """
        logging.info("Running %s..." % str(self.__class__.__name__))

        power_states_dict = {}
        assignment_dict = {}

        # monitor network traffic of all APs
        self.monitor_traffic(ap_list)

        # as starting point: assign all UEs to APs which have display_state!=0
        for ue in ue_list:
            if ue["display_state"] != 0:
                closest_ap = self.find_closest_ap(ue, ap_list)
                if closest_ap is not None:
                    assignment_dict[ue["uuid"]] = closest_ap["uuid"]

        # if throughput threshold of one AP is exceeded, power on that
        # AP which has the smallest distance to the farthest UE from
        # this AP, and mover the UE to that AP.
        # (BCGDemo special case: only moves one UE)
        for ap in ap_list:
            if self.get_avg_traffic(ap["uri"]) > self.THRESHOLD:
                ap_list_without_ap = list(ap_list)
                ap_list_without_ap.remove(ap)
                # find UE that should be moved away from this AP
                fue = self.find_farthest_ue(ap, ue_list)
                logging.debug("AP: %s has farthest UE: %s" % (ap["device_id"],
                                                              str(fue)))
                # calculate to which alternative AP the UE should be connected
                if fue is not None:
                    new_ap = self.find_closest_ap(fue, ap_list)
                    if new_ap is not None:
                        assignment_dict[fue["uuid"]] = new_ap["uuid"]
                        logging.debug("Moved UE: %s to: %s" %
                                      (fue["device_id"], new_ap["device_id"]))

        # switch on all APs which are assigned to at least on UE
        for ap in ap_list:
            if ap["uuid"] in assignment_dict.itervalues():
                power_states_dict[ap["uuid"]] = True
            else:  # turn off all unassigned APs
                power_states_dict[ap["uuid"]] = False

        # return({}, {})
        return (power_states_dict, assignment_dict)
