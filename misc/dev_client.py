import IPython
import requests
import json
import random
import time

DOC = """
This is a interactive client to interact with the network controller
component. It opens a IPython shell and provides helper functions
to do UE, AP, location, or Network requests to the controller API.

Usable Objects / Methods:
    - API_HOST: API host address
    - API_PORT: API port
    - NETWORK_API_HOST: Network manager API host address
    - NETWORK_API_PORT: Network manager API port
    - UEDATA is a dictionary containing default UE request values.

    - UE is a request object providing the following helper methods:
        * url = UE.register(data=UEDATA) # register UE at controller
        * UE.update(url, data=UEDATA)    # send status update
        * UE.remove(url)                # remove UE from
        * UE.list()                     # returns list of all UE urls
        * UE.get(url)                   # gets specific UE data

    - AP is a request object providing the following helper methods:
        * AP.list()                     # returns list of all AP urls
        * AP.get(url)                   # gets specific AP data

    - LOC is a request object providing the following helper methods:
        * LOC.post(location_service_id, p_x, p_y) # posts location

    - NW is a request object providing the following helper methods:
        * NW.list()                     # returns list of all AP uuids
        * NW.get(uuid)                  # gets specific AP data (NW.get(_[0]))
        * NW.set_mac_list(mac, enable_on, disable_on)
                                        # enables / disables mac on APs,
                                        # use (uuid lists)
        * NW.enable_mac_on(mac, apidx)  # enables given mac only on AP which is
                                        # specified by its index in the AP list

"""

API_HOST = "127.0.0.1"
API_PORT = "6680"

NETWORK_API_HOST = "127.0.0.1"
NETWORK_API_PORT = "6681"

UEDATA = {
    "device_id": "Test UE",
    "location_service_id": "tcnode1",
    "position_x": 0,
    "position_y": 0,
    "display_state": 1,
    "active_application_package": "com.android.browser",
    "wifi_mac": "00:8a:32:ce:fd:7e"
}


class UE_Request(object):
    """
    - UE is a request object providing the following helper methods:
        * url = UE.register(data=UEDATA) # register UE at controller
        * UE.update(url, data=UEDATA)    # send status update
        * UE.remove(url)                # remove UE from
        * UE.list()                     # returns list of all UE urls
        * UE.get(url)                   # gets specific UE data
    """

    def __init__(self):
        # store all created UEs, in order to force removal at exit
        self.ue_list = []

    def _get_url(self):
        return "http://%s:%s" % (API_HOST, API_PORT)

    def register(self, data=UEDATA):
        r = requests.post(
            self._get_url() + "/api/ue",
            data=json.dumps(data))
        assert(r.status_code == 201)
        url = r.json()[0]
        self.ue_list.append(url)
        return url

    def update(self, url, data=UEDATA):
        r = requests.put(self._get_url() + url,
                         data=json.dumps(data))
        assert(r.status_code == 204)

    def remove(self, url):
        r = requests.delete(self._get_url() + url)
        assert(r.status_code == 204)
        if url in self.ue_list:
            self.ue_list.remove(url)

    def list(self):
        r = requests.get(self._get_url() + "/api/ue")
        assert(r.status_code == 200)
        return r.json()

    def get(self, url):
        r = requests.get(self._get_url() + url)
        assert(r.status_code == 200)
        return r.json()

    def helper_register_n(self, n=5, data=UEDATA):
        """
        Helper. Registers n UEs at random positions.
        Helpful e.g. to test GUIs, which rely on data received
        from the backend's API.
        """
        for i in range(0, n):
            d = UEDATA.copy()
            # adapt UE values
            d["device_id"] += " " + str(i)
            d["position_x"] = random.uniform(0, 1000)
            d["position_y"] = random.uniform(0, 1000)
            self.register(data=d)

    def helper_remove_all(self):
        """
        Helper. Removes all UEs, which are currently registered
        in the backend.
        """
        l = self.list()
        for url in l:
            self.remove(url)


class AP_Request(object):
    """
    - AP is a request object providing the following helper methods:
        * AP.list()                     # returns list of all AP urls
        * AP.get(url)                   # gets specific AP data
    """

    def __init__(self):
        pass

    def _get_url(self):
        return "http://%s:%s" % (API_HOST, API_PORT)

    def list(self):
        r = requests.get(self._get_url() + "/api/accesspoint")
        assert(r.status_code == 200)
        return r.json()

    def get(self, url):
        r = requests.get(self._get_url() + url)
        assert(r.status_code == 200)
        return r.json()


class NW_Request(object):
    """
    - NW is a request object providing the following helper methods:
        * NW.list()                     # returns list of all AP uuids
        * NW.get(uuid)                  # gets specific AP data (NW.get(_[0]))
        * NW.set_mac_list(mac, enable_on, disable_on)
                                        # enables / disables mac on APs,
                                        # use (uuid lists)
        * NW.enable_mac_on(mac, apidx)  # enables given mac only on AP which is
                                        # specified by its index in the AP list
    """

    def __init__(self):
        pass

    def _get_url(self):
        return "http://%s:%s" % (NETWORK_API_HOST, NETWORK_API_PORT)

    def list(self, online_only=True):
        r = requests.get(self._get_url() + "/api/network/accesspoint")
        assert(r.status_code == 200)
        uuid_list = r.json()
        if online_only:
            return uuid_list["online"]
        else:
            return uuid_list["online"] + uuid_list["offline"]

    def get(self, uuid):
        r = requests.get(
            self._get_url() + "/api/network/accesspoint/%s" % uuid)
        assert(r.status_code == 200)
        return r.json()

    def set_mac_list(self, mac, enable_on, disable_on):
        assert(isinstance(enable_on, list))
        assert(isinstance(disable_on, list))
        cmd = {}
        cmd["enable_on"] = enable_on
        cmd["disable_on"] = disable_on
        print cmd
        r = requests.put(
            self._get_url() + "/api/network/client/" + str(mac),
            data=json.dumps(cmd))

    def enable_mac_on(self, mac="ff:ff:ff:ff:ff:ff", apidx=1):
        l1 = self.list()
        l2 = self.list()
        l2.remove(l2[apidx])
        self.set_mac_list(mac, [l1[apidx]], l2)


class LOC_Request(object):
    """
    - LOC is a request object providing the following helper methods:
        * LOC.post(location_service_id, p_x, p_y) # posts location
    """

    def __init__(self):
        pass

    def _get_url(self):
        return "http://%s:%s" % (API_HOST, API_PORT)

    def post(self, location_service_id="node1", p_x=0.0, p_y=0.0):
        cmd = {}
        cmd["location_service_id"] = location_service_id
        cmd["position_x"] = p_x
        cmd["position_y"] = p_y
        print cmd
        r = requests.post(
            self._get_url() + "/api/location",
            data=json.dumps(cmd))


class Random_Updater(object):
    """
    Randomly updates UEs.
    Used to test GUI.
    """

    def __init__(self):
        self.UE = UE_Request()

    def random_select_ue(self):
        ue_list = self.UE.list()
        if len(ue_list) < 1:
            return None
        random.shuffle(ue_list)
        return ue_list[0]

    def random_update_ue(self, ue_url):
        if ue_url is None:
            return
        d = self.UE.get(ue_url)
        # update data randomly:
        d["position_x"] = random.uniform(0, 1000)
        d["position_y"] = random.uniform(0, 1000)
        d["display_state"] = 0 if random.uniform(0, 100) < 40 else 1

        d["active_application_activity"] = random.sample(
            ['com.google.android.apps.youtube.app.WatchWhileActivity',
             'com.google.browser.Main'],  1)[0]
        d["active_application_package"] = random.sample(
            ['com.google.android.apps.youtube',
             'com.google.browser'],  1)[0]

        d["rx_mobile_bytes"] += random.uniform(0, 10000)
        d["rx_wifi_bytes"] += random.uniform(0, 10000)
        d["rx_total_bytes"] += random.uniform(0, 10000)
        d["rx_mobile_bytes_per_second"] = random.uniform(0, 1000)
        d["rx_wifi_bytes_per_second"] = random.uniform(0, 1000)
        d["rx_total_bytes_per_second"] = random.uniform(0, 1000)

        d["tx_mobile_bytes"] += random.uniform(0, 10000)
        d["tx_wifi_bytes"] += random.uniform(0, 10000)
        d["tx_total_bytes"] += random.uniform(0, 10000)
        d["tx_mobile_bytes_per_second"] = random.uniform(0, 1000)
        d["tx_wifi_bytes_per_second"] = random.uniform(0, 1000)
        d["tx_total_bytes_per_second"] = random.uniform(0, 1000)

        # send update request
        print "Updating UE: %s" % d["device_id"]
        self.UE.update(ue_url, data=d)

    def run(self):
        print "Starting continuous random updates (quit with ctrl+c)"
        while(1):
            ue_url = self.random_select_ue()
            self.random_update_ue(ue_url)
            time.sleep(2)


def main():
    print DOC
    # create helper request objects
    UE = UE_Request()
    AP = AP_Request()
    NW = NW_Request()
    LOC = LOC_Request()
    # helper for random updates
    RU = Random_Updater()
    # start interactive IPython shell
    IPython.embed()
    # force removal of all pending UEs
    for url in UE.ue_list:
        UE.remove(url)
        print "Removed UE: %s" % url
    UE.helper_remove_all()

if __name__ == '__main__':
    main()
