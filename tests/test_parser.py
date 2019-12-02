import os
import sys
from unittest import TestCase

from Core import Parser

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/../"+myPath)



class TestParser(TestCase):
    def test_parse_len(self):
        raw = "0002c90001c50000ff250"
        test = Parser(raw)
        self.assertDictEqual(
            test.parse(),
            {"Error": "Invalid Message length , {} != 24 ".format(len(raw))},
            "Length check",
        )

    def test_parse_1(self):
        test = Parser("3f0002c90001c50000ff2502")

        self.assertDictEqual(
            {
                "type": "BLE",
                "Station_1_id": 2,
                "Station_1_rssi": 201,
                "Station_2_id": 1,
                "Station_2_rssi": 197,
                "Station_3_id": 0,
                "Station_3_rssi": 255,
                "Battery": 25,
                "Magnet_status": 2,
            },
            test.parse(),
            "Valid Parsing",
        )

    def test_parse_2(self):
        test = Parser("3f0002ed0001e00000ff2502")

        self.assertDictEqual(
            {
                "type": "BLE",
                "Station_1_id": 2,
                "Station_1_rssi": 237,
                "Station_2_id": 1,
                "Station_2_rssi": 224,
                "Station_3_id": 0,
                "Station_3_rssi": 255,
                "Battery": 25,
                "Magnet_status": 2,
            },
            test.parse(),
            "Valid Parsing",
        )

    def test_unwanted(self):
        raw = "0c0002c90001c50000ff2502"
        test = Parser(raw)
        self.assertEqual(
            test.parse()["info"],
            'Unwanted data (Not BLE)',
            "Unwanted data check",
        )
