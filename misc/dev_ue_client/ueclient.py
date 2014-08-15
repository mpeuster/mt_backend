import IPython
import requests
import json

DOC = """
This is a interactive client to interact with the network controller
component. It opens a IPython shell and provides helper functions
to do UE requests to the controller API.

Usable Objects / Methods:
    - HOST: API host address
    - PORT: API port
    - RDATA is a dictionary containing default UE request values.
    - R is a request object providing the following helper methods:
        * url = R.register(data=RDATA) # register UE at controller
        * R.update(url, data=RDATA)    # send status update
        * R.remove(url)                # remove UE from
        * R.list()                     # returns list of all UE urls
        * R.get(url)                   # gets specific UE data

"""

HOST = "127.0.0.1"
PORT = "5000"

RDATA = {
    "device_id": "test-client-ue1",
    "location_service_id": "tcnode1",
    "position_x": 0,
    "position_y": 0,
    "display_state": 0,
    "active_application_package": "com.android.browser",
    "wifi_mac": "00:8a:32:ce:fd:7e"
}


class Request(object):
    """
    Request object:
        * url = R.register(data=RDATA) # register UE at controller
        * R.update(url, data=RDATA)    # send status update
        * R.remove(url)                # remove UE from
        * R.list()                     # returns list of all UE urls
        * R.get(url)                   # gets specific UE data
    """

    def __init__(self):
        # store all created UEs, in order to force removal at exit
        self.ue_list = []

    def _get_url(self):
        return "http://%s:%s" % (HOST, PORT)

    def register(self, data=RDATA):
        r = requests.post(
            self._get_url() + "/api/ue",
            data=json.dumps(data))
        assert(r.status_code == 201)
        url = r.json()[0]
        self.ue_list.append(url)
        return url

    def update(self, url, data=RDATA):
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

# TODO: Add Helper class, providing methods like: register_n(n, data=RDATA)


def main():
    print DOC
    # create helper request object
    R = Request()
    # start interactive IPython shell
    IPython.embed()
    # force removal of all pending UEs
    for url in R.ue_list:
        R.remove(url)
        print "Removed UE: %s" % url

if __name__ == '__main__':
    main()
