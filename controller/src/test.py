import json
import unittest
import requests
import subprocess
import time

"""
Test ideas:
- make test create ue helper: ok
- create several ue: ok
- check ue result data: ok
- check PUT function: ok
- check DELETE function: ok
- create duplicated ue: ok
- create ue with wrong data

"""

API_BASE_URL = "http://127.0.0.1:5000"

REQUEST_DATA_1 = {
    "device_id": "device-static-1",
    "location_service_id": "node1",
    "position_x": 0,
    "position_y": 0,
    "display_state": 0,
    "active_application": "com.android.browser"
}

REQUEST_DATA_2 = {
    "device_id": "device-static-2",
    "location_service_id": "node2",
    "position_x": 999.001,
    "position_y": -999.999,
    "display_state": 1,
    "active_application": "com.google.youtube"
}


class UE_InterfaceTest(unittest.TestCase):

    """
    Test setup and tear down:
    """
    def setUp(self):
        """
        Creates some user equipment (UE) resources.
        """
        self.request_data = REQUEST_DATA_1
        self.request_data2 = REQUEST_DATA_2
        self._helper_create_n_ues(5)

    def tearDown(self):
        """
        Deletes all existing UEs.
        """
        for url in helper_get_ue_list():
            helper_delete_ue(url)
        self.assertEqual(len(helper_get_ue_list()), 0)

    """
    Tests:
    """
    def test_get_ues(self):
        data = helper_get_ue_list()
        # check response
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 5)
        # check all ue resources in list
        for url in data:
            helper_get_ue(url)

    def test_validate_ue_data(self):
        # create test ue
        r = helper_create_ue()
        url = json.loads(r.json())[0]
        # get new ue
        ue_data = helper_get_ue(url)
        # check if initial data is valid and unchanged in response
        for k, v in self.request_data.items():
            self.assertTrue(k in ue_data)
            self.assertEqual(v, ue_data[k])
        # check for existence of additional response fields
        self.assertTrue("uuid" in ue_data)
        # remove test ue
        helper_delete_ue(url)

    def test_update_ue(self):
        # create test ue
        r = helper_create_ue()
        url = json.loads(r.json())[0]
        # update request
        r = requests.put(API_BASE_URL + url,
                         data=json.dumps(self.request_data2))
        # check response
        self.assertEqual(r.status_code, 204)
        # get updated ue
        ue_data = helper_get_ue(url)
        # check if new data is valid and included in response
        for k, v in self.request_data2.items():
            self.assertTrue(k in ue_data)
            self.assertEqual(v, ue_data[k])
        # check for existence of additional response fields
        self.assertTrue("uuid" in ue_data)
        # remove test ue
        helper_delete_ue(url)

    def test_insert_duplicated_ue(self):
        r = helper_create_ue("test_duplicate")
        self.assertEqual(r.status_code, 201)
        r = helper_create_ue("test_duplicate")
        self.assertEqual(r.status_code, 409)

    def test_context_list(self):
        # create test ue
        r = helper_create_ue()
        url = json.loads(r.json())[0]
        # make update to create second context
        r = requests.put(API_BASE_URL + url,
                         data=json.dumps(self.request_data2))
        # get context list
        r = requests.get(API_BASE_URL + url + "/context")
        clist = json.loads(r.json())
        self.assertGreaterEqual(len(clist), 2)
        for curl in clist:
            r = requests.get(API_BASE_URL + curl)
            data = json.loads(r.json())
            # check response
            self.assertEqual(r.status_code, 200)
            # check if new data is valid and included in response
            for k, v in self.request_data2.items():
                self.assertTrue(k in data)

    """
    Helper functions:
    """
    def _helper_create_n_ues(self, n):
        for i in range(0, n):
            r = helper_create_ue("device-%s" % str(i + 1))
            data = json.loads(r.json())
            # check response
            self.assertEqual(r.status_code, 201)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            # check new created ue resource
            helper_get_ue(data[0])


class Location_InterfaceTest(unittest.TestCase):
    """
    Test setup and tear down:
    """
    def setUp(self):
        r = helper_create_ue(
            device_id="loc_ue1", location_service_id="loc_node1")
        data = json.loads(r.json())
        self.assertIsInstance(data, list)
        self.ue_url = data[0]

    def tearDown(self):
        """
        Deletes all existing UEs.
        """
        for url in helper_get_ue_list():
            helper_delete_ue(url)
        self.assertEqual(len(helper_get_ue_list()), 0)
    """
    Tests:
    """
    def test_set_location(self):
        # data definition
        data = {
            "location_service_id": "loc_node1",
            "position_x": 123.999,
            "position_y": 456.111
        }
        # first (create) request
        r = requests.post(API_BASE_URL + "/api/location",
                          data=json.dumps(data))
        self.assertEqual(r.status_code, 201)
        # second (update) request
        data["position_x"] = 200.01
        data["position_y"] = 100.99
        r = requests.post(API_BASE_URL + "/api/location",
                          data=json.dumps(data))
        self.assertEqual(r.status_code, 201)
        # check if the position is available at UE
        ue = helper_get_ue(self.ue_url)
        self.assertEqual(ue["position_x"], 200.01)
        self.assertEqual(ue["position_y"], 100.99)


class AccessPoint_InterfaceTest(unittest.TestCase):
    """
    Test setup and tear down:
    """
    def setUp(self):
        """
        Creates some user equipment (UE) resources.
        """
        for i in range(0, 3):
            helper_create_ue("ue%d" % i)

    def tearDown(self):
        """
        Deletes all existing UEs.
        """
        for url in helper_get_ue_list():
            helper_delete_ue(url)
        self.assertEqual(len(helper_get_ue_list()), 0)

    """
    Tests:
    """
    def test_get_accesspoints(self):
        # get list
        r = requests.get(API_BASE_URL + "/api/accesspoint")
        data = json.loads(r.json())
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(data, list)
        for url in data:
            r = requests.get(API_BASE_URL + url)
            ap = json.loads(r.json())
            self.assertEqual(r.status_code, 200)
            self.assertIsInstance(ap, dict)
            self.assertTrue("device_id" in ap)
            print ap

"""
Global Helper
"""


def helper_create_ue(device_id=None, location_service_id=None):
    data = REQUEST_DATA_1.copy()
    if device_id:
        data["device_id"] = device_id
    if location_service_id:
        data["location_service_id"] = location_service_id
    return requests.post(API_BASE_URL + "/api/ue",
                         data=json.dumps(data))


def helper_delete_ue(url):
        r = requests.delete(API_BASE_URL + url)
        assert(r.status_code == 204)


def helper_get_ue(url):
    r = requests.get(API_BASE_URL + url)
    data = json.loads(r.json())
    # check response
    assert(r.status_code == 200)
    assert(type(data) is dict)
    # print data
    return data


def helper_get_ue_list():
        r = requests.get(API_BASE_URL + "/api/ue")
        data = json.loads(r.json())
        assert(r.status_code == 200)
        assert(type(data) is list)
        return data


if __name__ == '__main__':
    if subprocess.call(
            ["python", "mnt2api.py", "-l", "debug", "-a", "restart"]) == 0:
        print "Waiting 1s to start tests..."
        time.sleep(1)  # wait to start process
        unittest.main()
