from unittest import TestCase

from Core import Station_Config, Coordinates
from main import find_location


def make_test_stations():
    return [
        Station_Config(
            station_name="station_1_pos", coordinates=Coordinates(x=47, y=7)
        ),
        Station_Config(
            station_name="station_2_pos", coordinates=Coordinates(x=34, y=5)
        ),
        Station_Config(
            station_name="station_3_pos", coordinates=Coordinates(x=12, y=37)
        ),
    ]


input = {
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
    },
    "timestamp": 1576068661.663207,
}
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
    },
    "timestamp": 1576068661.663207,
    "location": {
        "x": -24.07608695652174,
        "y": 0.7445652173913043,
        "ref_station_1_pos": {"x": 47.0, "y": 7.0},
        "ref_station_2_pos": {"x": 34.0, "y": 5.0},
        "ref_station_3_pos": {"x": 12.0, "y": 37.0},
    },
}


class TestFind_location(TestCase):
    def test_find_location(self):
        self.assertDictEqual(output, find_location(data=input, test_stations=make_test_stations()))
