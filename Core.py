from datetime import datetime

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


def get_station_config(station, Config_root):
    """
    Read A Doc from Config_root object Aka Firestore Collection
    :param Config_root: root of the Config
    :param station: Doc Title , name , string
    :return: Station_Config object
    """
    station_1_conf = Config_root.document(station)
    doc = station_1_conf.get()
    if doc.to_dict():
        cords = Coordinates(**doc.to_dict())
    else:
        # 9999 , 9999 means station not found
        cords = Coordinates(9999, 9999)
    return Station_Config(station_name=station, coordinates=cords)


def check_stations_cords(stations):
    not_found = 0
    for station in stations:
        x, y = station.get_coordinates()
        if x == 9999 and y == 9999:
            not_found += 1
    return "missing {} station(s) to do triangulation , received {} RSSIs \n".format(not_found, 3 - not_found) if \
        not_found else \
        False


def get_all__station_configs(Config_root):
    Configs = {}
    docs = Config_root.stream()
    for doc in docs:
        if "station_" in doc.id:
            Configs[doc.id] = get_station_config(doc.id, Config_root)

    return Configs


# TODO remove boilerplate Code
# def fill_fake_stations():
#     for i in range(1, 20):
#         Config_root.document("station_{}_pos".format(i)).set({"x": randint(0, 50), "y": randint(0, 50)})



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


class Coordinates:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "<Coordinates Object x : {} | y : {}>".format(self.x, self.y)


class Station_Config(object):
    def __init__(self, station_name, coordinates):
        self.station_name = station_name
        self.x = coordinates.x
        self.y = coordinates.y

    def get_coordinates(self):
        return self.x, self.y

    def __repr__(self):
        return "<Station_Config Object  station_name : {} | x : {} | y : {}>".format(
            self.station_name, self.x, self.y
        )

def get_all_stations(DataParsed):
    from configuration import Config_root
    return [
        get_station_config(
            "station_{}_pos".format(DataParsed["Station_{}_id".format(id)]),
            Config_root,
        )
        for id in range(1, 4)
    ]


def parse(data):
    parser = Parser(raw_data=data["data"])
    data["parsed"] = parser.parse()
    data["timestamp"] = datetime.timestamp(datetime.now())
    return data


def find_location(data, test_stations=None):
    data["location"] = {}
    if data["parsed"]["type"] == "BLE":
        station_pos = test_stations if test_stations else get_all_stations(data["parsed"])
        check = check_stations_cords(stations=station_pos)
        if check:
            data["location"]["message"] = check
            data["location"]["status"] = False

        else:
            trilaterate = trilaterator(
                station_1_pos=station_pos[0].get_coordinates(),
                rssi_1=data["parsed"]["Station_1_rssi"],
                station_2_pos=station_pos[1].get_coordinates(),
                rssi_2=data["parsed"]["Station_2_rssi"],
                station_3_pos=station_pos[2].get_coordinates(),
                rssi_3=data["parsed"]["Station_3_rssi"],
            )
            x, y = trilaterate.get_position()
            data["location"] = {
                "status": True,
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

    else:
        data["location"]["message"] = "BLE Data Required"
        data["location"]["status"] = False
    return data
