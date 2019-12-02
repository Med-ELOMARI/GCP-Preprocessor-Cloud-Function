from flask import jsonify
from datetime import datetime

from Core import Parser, validate
from configuration import data_root, Config_root


def main(request):
    try:
        data = request.get_json()
        result = validate(data)

        if result is "payload":
            parser = Parser(raw_data=data["data"])
            data["parsed"] = parser.parse()
            data["timestamp"] = datetime.timestamp(datetime.now())
            data_root.document(data["time"]).set(data)
            return jsonify(data), 200
        elif result is "Config":
            for station, cord in data["Config"].items():
                Config_root.document(station).set(cord)
            data["Status"] = "Config Writen Successfully "
            return jsonify(data), 200
        else:
            validate("")

    except Exception as e:
        return (
            jsonify(
                {
                    "Error": "Unexpected Error Occurred While processing the Message",
                    "Details": str(e),
                }
            ),
            500,
        )
