import json
import unittest
import requests
import subprocess
import time

API_BASE_URL = "http://127.0.0.1:6681"


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
        # get list of AP uuids:
        r = requests.get(API_BASE_URL + "/api/network/accesspoint")
        self.assertEqual(r.status_code, 200)
        aps = r.json()
        # enable and disable some APs for this mac:
        mac = "00:11:aa:bb:22:cc"
        cmd = {}
        cmd["enable_on"] = [uuid for uuid in aps["online"]]
        cmd["disable_on"] = []
        r = requests.put(
            API_BASE_URL + "/api/network/client/" + mac,
            data=json.dumps(cmd))
        self.assertEqual(r.status_code, 204)
        cmd["enable_on"] = []
        cmd["disable_on"] = [uuid for uuid in aps["online"]]
        r = requests.put(
            API_BASE_URL + "/api/network/client/" + mac,
            data=json.dumps(cmd))
        self.assertEqual(r.status_code, 204)

    def test_get_info(self):
        print "#" * 20
        r = requests.get(API_BASE_URL + "/api/network/accesspoint")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIsInstance(data, dict)
        print data
        for uuid in data["online"]:
            # check accesspoint endpoint get
            r_ap = requests.get(
                API_BASE_URL + "/api/network/accesspoint/" + uuid + "/info")
            self.assertEqual(r_ap.status_code, 200)
            data = r_ap.json()
            print data
            self.assertIsInstance(data, dict)
            self.assertTrue("name" in data)
            self.assertTrue("serial" in data)
            self.assertTrue("uuid" in data)

    def test_get_stats(self):
        r = requests.get(API_BASE_URL + "/api/network/accesspoint")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIsInstance(data, dict)
        print data
        for uuid in data["online"]:
            # check accesspoint endpoint get
            r_ap = requests.get(
                API_BASE_URL + "/api/network/accesspoint/" + uuid + "/stats")
            self.assertEqual(r_ap.status_code, 200)
            data = r_ap.json()
            print data
            self.assertIsInstance(data, dict)
            self.assertIsInstance(data["aps"], list)
            self.assertTrue(len(data["aps"]) > 0)
            for stats in data["aps"]:
                self.assertIsInstance(stats, dict)
                self.assertTrue("rxbyte" in stats)
                self.assertTrue("rxpkt" in stats)
                self.assertTrue("txbyte" in stats)
                self.assertTrue("txpkt" in stats)
                self.assertTrue("name" in stats)
                self.assertTrue("timestamp" in stats)


def setUpModule():
    if subprocess.call(
            ["python", "upb_apmanager.py",
                "-l", "debug",
                "-a", "restart"]) > 0:
        print "upb_apmanger.py restart failed!"
        exit(1)
    print "Waiting 0.1s to start tests..."
    time.sleep(0.1)  # wait to start process


def tearDownModule():
    if subprocess.call(
            ["python", "upb_apmanager.py",
                "-l", "debug",
                "-a", "stop"]) > 0:
        print "upb_apmanger.py stop failed!"


if __name__ == '__main__':
    unittest.main()
