TYPES = {"0F": "None", "1F": "GPS", "2F": "WIFI", "3F": "BLE"}

payload_example = {"time": "must have", "Key1": "Value", "Key2": "Value"}
Config_example = {
    "Config": {
        "station_1_pos": {"x": 0, "y": 0},
        "station_2_pos": {"x": 6, "y": 5},
        "station_3_pos": {"x": 4, "y": 1},
    }
}


def validate(data):
    if not data:
        raise Exception(
            "No input was Provided , expected POST request with content-type : application/json and payload  {} "
            "or a Config Request {} ".format(str(payload_example), str(Config_example))
        )
    return (
        "payload"
        if check_key(data, "time")
        else "Config"
        if check_key(data, "Config")
        else fail(data)
    )


def fail(data):
    raise Exception(
        "time or Config keys must be included in the payload ! {}".format(data)
    )


def check_key(data, key):
    try:
        _ = data[key]
        return True
    except KeyError:
        return False


class Parser:
    """
    BLE Raw frame parser for Sigfox Device , return dict object example :
            3f0002c90001c50000ff2502
            0002 rssi: C9 = 201
            0001 rssi: C5 = 197
            3f0002ed0001e00000ff2502
            0002 rssi: ed = 237
            0001 rssi: e0 = 224
    Additional fields :
        Battery and magnet status:
        2502 -> 25 = 3.7v and 02 = Open

    """

    def __init__(self, raw_data):
        self.raw_data = str(raw_data)

    @staticmethod
    def get_type(input):
        try:
            return TYPES[str(input[0:2]).upper()]
        except KeyError:
            return "UNKNOWN"

    def get_integer(self, _from, _to):
        temp = self.raw_data[_from:_to]
        try:
            # converting using 10 base
            return int(temp)
        except (TypeError, ValueError):
            # converting using 16 base
            return int(temp, 16)

    def parse(self):

        if len(self.raw_data) != 24:
            return {
                "Error": "Invalid Message length , {} != 24 ".format(len(self.raw_data))
            }

        type = self.get_type(self.raw_data)

        if type is "BLE":
            return {
                "type": type,
                "Station_1_id": self.get_integer(2, 6),
                "Station_1_rssi": self.get_integer(6, 8),
                "Station_2_id": self.get_integer(8, 12),
                "Station_2_rssi": self.get_integer(12, 14),
                "Station_3_id": self.get_integer(14, 18),
                "Station_3_rssi": self.get_integer(18, 20),
                "Battery": self.get_integer(20, 22),
                "Magnet_status": self.get_integer(22, 24),
            }
        else:
            return {
                "type": type,
                "Message": self.raw_data,
                "info": "Unwanted data (Not BLE)",
            }


class trilaterator:
    def __init__(
        self, station_1_pos, rssi_1, station_2_pos, rssi_2, station_3_pos, rssi_3
    ):
        self.rssi_3 = rssi_3
        self.station_3_pos = station_3_pos

        self.rssi_2 = rssi_2
        self.station_2_pos = station_2_pos

        self.rssi_1 = rssi_1
        self.station_1_pos = station_1_pos

    def get_position(self):
        (x1, y1), (x2, y2), (x3, y3) = (
            self.station_1_pos,
            self.station_2_pos,
            self.station_3_pos,
        )
        A = 2 * x2 - 2 * x1
        B = 2 * y2 - 2 * y1
        C = self.rssi_1 ** 2 - self.rssi_2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
        D = 2 * x3 - 2 * x2
        E = 2 * y3 - 2 * y2
        F = self.rssi_2 ** 2 - self.rssi_3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2
        x = (C * E - F * B) / (E * A - B * D)
        y = (C * D - A * F) / (B * D - A * E)
        return x, y
