import logging
import threading
import time
import ap_manager_client
import model


class AccessPointStateFetcher(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        # fetch static information only once
        uuid_list = ["%s" % ap.uuid
                     for ap in model.accesspoint.AccessPoint.objects]
        for uuid in uuid_list:
                ap_info = ap_manager_client.get_accesspoint_info(uuid)
                model.accesspoint.AccessPoint.update_info(uuid, ap_info)

        while True:
            # periodically fetch network stats and write them to model
            logging.debug("Receiving access point updates")
            for uuid in uuid_list:
                ap_stats = ap_manager_client.get_accesspoint_stats(uuid)
                model.accesspoint.AccessPoint.update_stats(uuid, ap_stats)
            # wait for next update
            time.sleep(1)
