# Preprocessor using Cloud Function

![](https://github.com/Med-ELOMARI/GCP-Preprocessor-Cloud-Function/workflows/tests/badge.svg)
[![Build Status](https://travis-ci.com/Med-ELOMARI/GCP-Preprocessor-Cloud-Function.svg?branch=master)](https://travis-ci.com/Med-ELOMARI/GCP-Preprocessor-Cloud-Function)

This Repo host The **Preprocessor part** to handle requests received from Sigfox network (Callbacks) 

# Flow

![GCP cloudFunction(1)](https://user-images.githubusercontent.com/11338137/69978600-08964980-152d-11ea-8ad7-8477979bfcc3.png)


- input is a Json and Must Contain a time key 
```json
{"time": "must have", "data": "Value", "Key2": "Value2","Key3": "Value3" } 
```

- The output is Json with parsed elements also ( will be writen also to DB firestore) 

# How To Deploy

Setup gcloud console 
 
Make sure there is a Firestore DB created in the same GCP Project

```cmd
gcloud functions deploy Preprocessor --entry-point main --runtime python37 --trigger-http 
```

**Note : No need to have Firestore credentials , everything internally managed By GCP**

