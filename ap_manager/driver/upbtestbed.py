import logging
import subprocess
import time


class ApDriver():

    def __init__(self):
        logging.info("[ApDriver] UpbTestbed driver loaded.")

    def set_mac_lists(self, ap):
        """
        ATTENTION: Mac blacklisting not used at the moment,
        because hostapd disconnects all clients whenever its configuration
        files are reloaded. A better solution for assigning UEs to specific
        APs is using BSSIDs on the client to directly choose the target AP.
        """
        assert(ap.driver_info is not None)
        assert("ssh_name" in ap.driver_info)

        logging.info("[ApDriver] Setting MAC lists for %s" % ap)

        ###########################
        return  # #### DEACTIVATED!
        ###########################

        # get ssh shortcut name for AP
        ssh_name = ap.driver_info["ssh_name"]

        # write local accept file
        f = open('/tmp/mac.accept', 'w')
        f.write("\n".join(ap.enabled_macs))
        f.close()
        # write local deny file
        f = open('/tmp/mac.deny', 'w')
        f.write("\n".join(ap.disabled_macs))
        f.close()
        # copy both files to access point
        subprocess.call(
            "scp /tmp/mac.accept %s:/etc/hostapd/mac.accept" % ssh_name,
            shell=True)
        subprocess.call(
            "scp /tmp/mac.deny %s:/etc/hostapd/mac.deny" % ssh_name,
            shell=True)
        # send signal to hostapd process to trigger config reload
        subprocess.call(
            "ssh -n %s 'pkill -HUP hostapd'" % ssh_name,
            shell=True)

    def set_power_state(self, ap):
        logging.info("[ApDriver] Setting power state for %s to: %s"
                     % (ap, ap.power_state))

    def get_power_state(self, ap):
        logging.info("[ApDriver] Getting power state for %s" % ap)
        # ATTENTION: Never called!
        return "radio_on"

    def get_network_stats(self, ap):
        logging.info("[ApDriver] Getting networks stats for %s" % ap)
        return {"aps": [
                {"name": "vap0",
                 "rxbyte": 1234,
                 "rxpkt": 123,
                 "txbyte": 6789,
                 "txpkt": 678,
                 "timestamp": time.time()
                 }]}
