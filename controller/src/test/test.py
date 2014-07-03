import json
import unittest
import requests

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
    "position_x": 999,
    "position_y": -999,
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
        for url in self._helpter_get_ue_list():
            self._helper_delete_ue(url)
        self.assertEqual(len(self._helpter_get_ue_list()), 0)

    """
    Tests:
    """
    def test_get_ues(self):
        data = self._helpter_get_ue_list()
        # check response
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 5)
        # check all ue resources in list
        for url in data:
            self._helper_get_specific_ue(url)

    def test_validate_ue_data(self):
        # create test ue
        r = self._helper_create_new_ue()
        url = json.loads(r.json())[0]
        # get new ue
        ue_data = self._helper_get_specific_ue(url)
        # check if initial data is valid and unchanged in response
        for k, v in self.request_data.items():
            self.assertTrue(k in ue_data)
            self.assertEqual(v, ue_data[k])
        # check for existence of additional response fields
        self.assertTrue("uuid" in ue_data)
        # remove test ue
        self._helper_delete_ue(url)

    def test_update_ue(self):
        # create test ue
        r = self._helper_create_new_ue()
        url = json.loads(r.json())[0]
        # update request
        r = requests.put(API_BASE_URL + url,
                         data=json.dumps(self.request_data2))
        # check response
        self.assertEqual(r.status_code, 204)
        # get updated ue
        ue_data = self._helper_get_specific_ue(url)
        # check if new data is valid and included in response
        for k, v in self.request_data2.items():
            self.assertTrue(k in ue_data)
            self.assertEqual(v, ue_data[k])
        # check for existence of additional response fields
        self.assertTrue("uuid" in ue_data)
        # remove test ue
        self._helper_delete_ue(url)

    def test_insert_duplicated_ue(self):
        r = self._helper_create_new_ue("test_duplicate")
        self.assertEqual(r.status_code, 201)
        r = self._helper_create_new_ue("test_duplicate")
        self.assertEqual(r.status_code, 409)

    """
    Helper functions:
    """
    def _helper_get_specific_ue(self, url):
        r = requests.get(API_BASE_URL + url)
        data = json.loads(r.json())
        # check response
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(data, dict)
        return data

    def _helper_create_n_ues(self, n):
        for i in range(0, n):
            r = self._helper_create_new_ue("device-%s" % str(i + 1))
            data = json.loads(r.json())
            # check response
            self.assertEqual(r.status_code, 201)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            # check new created ue resource
            self._helper_get_specific_ue(data[0])

    def _helper_create_new_ue(self, device_id=None):
        data = self.request_data.copy()
        if device_id:
            data["device_id"] = device_id
        return requests.post(API_BASE_URL + "/api/ue",
                             data=json.dumps(data))

    def _helpter_get_ue_list(self):
        r = requests.get(API_BASE_URL + "/api/ue")
        data = json.loads(r.json())
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(data, list)
        return data

    def _helper_delete_ue(self, url):
        r = requests.delete(API_BASE_URL + url)
        # check response
        self.assertEqual(r.status_code, 204)

if __name__ == '__main__':
    unittest.main()
