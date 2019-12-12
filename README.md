# Preprocessor using Cloud Function

[![CircleCI](https://circleci.com/gh/Med-ELOMARI/GCP-Preprocessor-Cloud-Function/tree/master.svg?style=svg)](https://circleci.com/gh/Med-ELOMARI/GCP-Preprocessor-Cloud-Function/tree/master)
![](https://github.com/Med-ELOMARI/GCP-Preprocessor-Cloud-Function/workflows/tests/badge.svg)
[![Build Status](https://travis-ci.com/Med-ELOMARI/GCP-Preprocessor-Cloud-Function.svg?branch=master)](https://travis-ci.com/Med-ELOMARI/GCP-Preprocessor-Cloud-Function)
[![codecov](https://codecov.io/gh/Med-ELOMARI/GCP-Preprocessor-Cloud-Function/branch/master/graph/badge.svg)](https://codecov.io/gh/Med-ELOMARI/GCP-Preprocessor-Cloud-Function)



This Repo host The **Preprocessor part** to handle requests received from Sigfox network (Callbacks) 

# Flow

![GCP cloudFunction(1)](https://user-images.githubusercontent.com/11338137/69978600-08964980-152d-11ea-8ad7-8477979bfcc3.png)


- input is a Json and Must Contain a time key 
```json
{"time": "must have", "data": "Value", "Key2": "Value2","Key3": "Value3" } 
```

- The output is Json with parsed elements and calculated Location if possible  also it will be writen to
 firestore on the same Project

# How To Deploy

1. Setup gcloud console and Create a Project on GCP

2. Clone this Repository 

3. Define environment variables for the Command or Specify them in configuration.py like **PROJECT_NAME** and other
 Fields (you can specify Data  routes ... aka collections routes)
 
4. Make sure there is a Firestore DB created in the same GCP Project

5. Run The command (with ENV=prod also you can Add the other environment variables)
```cmd
gcloud functions deploy Preprocessor --entry-point main --runtime python37 --trigger-http  --set-env-vars ENV=prod --allow-unauthenticated
```

Finally you can Get Function Url by
```cmd
gcloud functions describe Preprocessor
```

```yaml
availableMemoryMb: 256
entryPoint: main
httpsTrigger:
  url: https://REGION-PROJECT_NAME.cloudfunctions.net/Preprocessor
...
...
versionId: "1"
```

Last step is to add The link to Sigfox Callbacks URl and specify a valid payload with POST request 

**Note : No need to have Firestore credentials , everything internally managed By GCP**

# Example 

input 
```json
{
    "time": "1576077223",
    "device": "336B67",
    "data": "3f0002d50003c50001c32402"
}
``` 
output 

```json
{
    "time": "1576077223",
    "device": "336B67",
    "data": "3f0002d50003c50001c32402",
    "parsed": {
        "type": "BLE",
        "Station_1_id": 2,
        "Station_1_rssi": 213,
        "Station_2_id": 3,
        "Station_2_rssi": 197,
        "Station_3_id": 1,
        "Station_3_rssi": 195,
        "Battery": 24,
        "Magnet_status": 2
    },
    "timestamp": 1576163534.164381,
    "location": {
        "status": True,
        "x": 277.9217391304348,
        "y": 298.7586956521739,
        "ref_station_2_pos": {
            "x": 34.0,
            "y": 5.0
        },
        "ref_station_3_pos": {
            "x": 12.0,
            "y": 37.0
        },
        "ref_station_1_pos": {
            "x": 47.0,
            "y": 7.0
        }
    }
}
```
**Note : Stations Positions *(ref_station_X_pos)*  are needed to calculate the position *(using Trilateration)* and are
 located in  firestore
 DB inside TheCollection Config**