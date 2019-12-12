import os
import sys

from flask import jsonify

from Core import validate, parse, find_location


def main(request, test=False):
    try:
        # to be able to test the function locally , added the test parameter

        data = request if test else request.get_json()

        result = validate(data)

        if result is "payload":

            data = parse(data=data)
            print(data)

            data = find_location(data=data)

            from configuration import data_root

            data_root.document(data["time"]).set(data)

            print(data)

            return jsonify(data), 200
        elif result is "Config":
            for station, cord in data["Config"].items():
                from configuration import Config_root

                Config_root.document(station).set(cord)
            data["Status"] = "Config Writen Successfully "
            return jsonify(data), 200
        else:
            validate("")

    except Exception as e:
        if test:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, sys.exc_info())
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
    request = {"time": "1576077223", "device": "336B67", "data": "3f0002d50003c50001c32402"}
    try:
        ENV = os.getenv("ENV", "dev")
        test = True if ENV == "dev" or ENV == "test" else False
        main(request, test=test)
    except RuntimeError:
        # Flask Context Error , Passed for testing
        pass
