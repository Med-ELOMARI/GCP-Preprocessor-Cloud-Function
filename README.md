# Preprocessor using Cloud Function

![](https://github.com/Med-ELOMARI/GCP-Preprocessor-Cloud-Function/workflows/tests/badge.svg)

This Repo host The **Preprocessor part** to handle requests received from Sigfox network (Callbacks) 

# Flow

![GCP cloudFunction](https://user-images.githubusercontent.com/11338137/69967196-32914100-1518-11ea-9862-5a865dba9804.png)


# How To Deploy

Setup gcloud console 
 
Make sure there is a Firestore DB created in the same GCP Project

```cmd
gcloud functions deploy Preprocessor --entry-point main --runtime python37 --trigger-http 
```

**Note : No need to have Firestore credentials , everything internally managed By GCP**
