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
        """
        Fetches network stats from access point.
        Done by executing and greping ifconfig via ssh.
        TODO: Find a better solution. This is just a quick hack.
        """
        logging.info("[ApDriver] Getting networks stats for %s" % ap)
        # get ssh shortcut name for AP
        ssh_name = ap.driver_info["ssh_name"]
        # get information about rx/tx bytes from remote ifconfig
        proc = subprocess.Popen(
            "ssh -n %s 'ifconfig wlan0 | grep bytes'" % ssh_name,
            shell=True,
            stdout=subprocess.PIPE)
        # parse results
        new_stats = self.__parse_ifconfig_output(proc.stdout.readline())
        # build return dict
        rxb = 0
        txb = 0
        if "rx_bytes" in new_stats:
            rxb = new_stats["rx_bytes"]
        if "tx_bytes" in new_stats:
            txb = new_stats["tx_bytes"]

        return {"aps": [
                {"name": "wlan0",
                 "rxbyte": rxb,
                 "rxpkt": 0,  # packets are not counted by this driver
                 "txbyte": txb,
                 "txpkt": 0,  # packets are not counted by this driver
                 "timestamp": time.time()
                 }]}

    def __parse_ifconfig_output(self, line):
        """
        Parses ifconfig output line to receive current bytecount.
        """
        if line is None or len(line) < 10:
            return {}
        rxb = 0
        txb = 0
        parts = line.split(" ")
        found = 0
        try:
            for p in parts:
                if "bytes:" in p:
                    subparts = p.split(":")
                    if found < 1:
                        rxb = int(subparts[1])
                        found += 1
                    else:
                        txb = int(subparts[1])
        except:
            rxb = 0
            txb = 0

        return {"rx_bytes": rxb, "tx_bytes": txb}
