import os
import sys
from datetime import datetime

from flask import jsonify

from Core import (
    Parser,
    validate,
    get_station_config,
    trilaterator,
    check_stations_cords,
)
from configuration import Config_root, data_root


def main(request, test=False):
    try:
        # to be able to test the function locally , added the test parameter
        if test:
            data = request
        else:
            data = request.get_json()

        result = validate(data)

        if result is "payload":
            parser = Parser(raw_data=data["data"])
            DataParsed = parser.parse()
            data["parsed"] = DataParsed
            data["timestamp"] = datetime.timestamp(datetime.now())
            station_pos = [
                get_station_config(
                    "station_{}_pos".format(DataParsed["Station_{}_id".format(id)]),
                    Config_root,
                )
                for id in range(1, 4)
            ]

            check = check_stations_cords(stations=station_pos)
            if check:
                data["location"] = check
            else:
                trilaterate = trilaterator(
                    station_1_pos=station_pos[0].get_coordinates(),
                    rssi_1=DataParsed["Station_1_rssi"],
                    station_2_pos=station_pos[1].get_coordinates(),
                    rssi_2=DataParsed["Station_2_rssi"],
                    station_3_pos=station_pos[2].get_coordinates(),
                    rssi_3=DataParsed["Station_3_rssi"],
                )
                x, y = trilaterate.get_position()
                data["location"] = {
                    "x": x,
                    "y": y,
                    "ref_{}".format(station_pos[0].station_name): {
                        "x": station_pos[0].get_coordinates()[0],
                        "y": station_pos[0].get_coordinates()[1],
                    },
                    "ref_{}".format(station_pos[1].station_name): {
                        "x": station_pos[1].get_coordinates()[0],
                        "y": station_pos[1].get_coordinates()[1],
                    },
                    "ref_{}".format(station_pos[2].station_name): {
                        "x": station_pos[2].get_coordinates()[0],
                        "y": station_pos[2].get_coordinates()[1],
                    },
                }

            data_root.document(data["time"]).set(data)
            print(data)
            return jsonify(data), 200
        elif result is "Config":
            for station, cord in data["Config"].items():
                Config_root.document(station).set(cord)
            data["Status"] = "Config Writen Successfully "
            return jsonify(data), 200
        else:
            validate("")

    except Exception as e:
        if test:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        return (
            jsonify(
                {
                    "Error": "Unexpected Error Occurred While processing the Message",
                    "Details": str(e),
                }
            ),
            500,
        )


if __name__ == "__main__":
    request = {"time": "Test6", "device": "336B67", "data": "3f0001900002800003752502"}
    try:
        main(request, test=True)
    except RuntimeError:
        # Flask Context Error , Passed for testing
        pass
