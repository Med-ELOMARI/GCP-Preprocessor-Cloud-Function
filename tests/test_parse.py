from unittest import TestCase

from main import parse

input = {"time": "Test", "device": "336B67", "data": "3f0001900002800003752502"}
output = {
    "time": "Test",
    "device": "336B67",
    "data": "3f0001900002800003752502",
    "parsed": {
        "type": "BLE",
        "Station_1_id": 1,
        "Station_1_rssi": 90,
        "Station_2_id": 2,
        "Station_2_rssi": 80,
        "Station_3_id": 3,
        "Station_3_rssi": 75,
        "Battery": 25,
        "Magnet_status": 2,
    }
}

class TestParse(TestCase):
    def test_parse(self):
        parsed = parse(input)
        self.assertIn("timestamp", parsed)
        del parsed["timestamp"]
        self.assertDictEqual(parsed, input)
