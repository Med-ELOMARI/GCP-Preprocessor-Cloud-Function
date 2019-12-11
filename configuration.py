import os

from firebase_admin import credentials, firestore, initialize_app

ENV = os.getenv("ENV", "prod")

PROJECT_NAME = "nektiu-4280d"

# initialize firebase sdk
CREDENTIALS = credentials.ApplicationDefault()
default_app = (
    initialize_app(CREDENTIALS, {"projectId": PROJECT_NAME})
    if ENV == "prod"
    else initialize_app(credentials.Certificate("local/nektiu-db.json"))
)


FIRESTORE_CLIENT = firestore.client()

data_root = FIRESTORE_CLIENT.collection("Sigfox")
Config_root = FIRESTORE_CLIENT.collection("Config")
