import IPython
import requests
import json

DOC = """
This is a interactive client to interact with the network controller
component. It opens a IPython shell and provides helper functions
to do UE or Network requests to the controller API.

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

    - NW is a request object providing the following helper methods:
        * NW.list()                     # returns list of all AP uuids
        * NW.get(uuid)                  # gets specific AP data (NW.get(_[0]))
        * NW.set_mac_list(mac, enable_on, disable_on)
                                        # enables / disables mac on APs,
                                        # use (uuid lists)
        * NW.enable_mac_on(mac, apidx)  # enables given mac only on AP which is
                                        # specified by its index in the AP list

    - LOC is a request object providing the following helper methods:
        * LOC.post(location_service_id, p_x, p_y) # posts location
"""

API_HOST = "127.0.0.1"
API_PORT = "6680"

NETWORK_API_HOST = "127.0.0.1"
NETWORK_API_PORT = "6681"

UEDATA = {
    "device_id": "test-client-ue1",
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

# TODO: Add Helper class, providing methods like: register_n(n, data=UEDATA)


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


def main():
    print DOC
    # create helper request objects
    UE = UE_Request()
    NW = NW_Request()
    LOC = LOC_Request()
    # start interactive IPython shell
    IPython.embed()
    # force removal of all pending UEs
    for url in UE.ue_list:
        UE.remove(url)
        print "Removed UE: %s" % url

if __name__ == '__main__':
    main()
