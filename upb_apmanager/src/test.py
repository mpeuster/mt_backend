import json
import unittest
import requests
import subprocess
import time

API_BASE_URL = "http://127.0.0.1:5001"


class AccessPoint_InterfaceTest(unittest.TestCase):
    """
    Test setup and tear down:
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    """
    Tests:
    """
    def test_get_on_all_endpoints(self):
        """
        Checks all get endpoints of API
        """
        # check list endpoint
        r = requests.get(API_BASE_URL + "/api/network/accesspoint")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIsInstance(data, dict)
        print data
        for uuid in data["online"]:
            # check accesspoint endpoint get
            r_ap = requests.get(
                API_BASE_URL + "/api/network/accesspoint/" + uuid)
            self.assertEqual(r_ap.status_code, 200)
            data = r_ap.json()
            print data
            self.assertIsInstance(data, dict)
            # check accesspoint endpoint power_state
            r_power_state = requests.get(
                API_BASE_URL + "/api/network/accesspoint/"
                + uuid + "/power_state")
            self.assertEqual(r_power_state.status_code, 200)
            data = r_power_state.json()
            print data
            self.assertIsInstance(data, dict)
            self.assertTrue("power_state" in data)

    def test_put_power_state(self):
        # get all access points
        r = requests.get(API_BASE_URL + "/api/network/accesspoint")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIsInstance(data, dict)
        for uuid in data["online"]:
            # change switch on all online aps
            cmd = {"power_state": "radio_on"}
            r = requests.put(
                API_BASE_URL + "/api/network/accesspoint/"
                + uuid + "/power_state", data=json.dumps(cmd))
            self.assertEqual(r.status_code, 204)
        for uuid in data["online"]:
            # change switch off all online aps
            cmd = {"power_state": "radio_off"}
            r = requests.put(
                API_BASE_URL + "/api/network/accesspoint/"
                + uuid + "/power_state", data=json.dumps(cmd))
            self.assertEqual(r.status_code, 204)

    def test_post_client_mac(self):
        pass


if __name__ == '__main__':
    if subprocess.call(
            ["python", "upb_apmanager.py",
                "-l", "debug",
                "-a", "restart"]) > 0:
        print "upb_apmanger.py restart failed! stopping tests."
        exit(1)
    print "Waiting 0.1s to start tests..."
    time.sleep(0.1)  # wait to start process
    unittest.main()
