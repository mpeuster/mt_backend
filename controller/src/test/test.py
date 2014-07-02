import json
import unittest
import requests

"""
Test ideas:
- make test create ue helper
- create several ue
- create duplicated ue
- create ue with wrong data

"""

API_BASE_URL = "http://127.0.0.1:5000"

REQUEST_DATA_1 = {
    "device_id": "device-identifier-1",
    "location_service_id": "node1",
    "position_x": 0,
    "position_y": 0,
    "display_state": 0,
    "active_application": "com.android.browser"
}


class UE_InterfaceTest(unittest.TestCase):

    def setUp(self):
        self.request_data = REQUEST_DATA_1

    def test_get_initial_list(self):
        r = requests.get(API_BASE_URL + "/api/ue")
        data = json.loads(r.json())

        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 0)

    def test_post_ue(self):
        r = requests.post(API_BASE_URL + "/api/ue",
                          data=json.dumps(self.request_data))
        data = json.loads(r.json())

        self.assertEqual(r.status_code, 201)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

        self._get_specific_ue(data[0])

    def _get_specific_ue(self, url):
        r = requests.get(API_BASE_URL + url)
        data = json.loads(r.json())

        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(data, dict)
        # self.assertTrue("uuid" in data)
        # self.assertTrue("device_id" in data)

        return data


if __name__ == '__main__':
    unittest.main()
