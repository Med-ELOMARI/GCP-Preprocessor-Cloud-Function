import os

from firebase_admin import credentials, firestore, initialize_app

ENV = os.getenv("ENV", "dev")
PROJECT_NAME = os.getenv("PROJECT_NAME", "nektiu-4280d")
Data_collection = os.getenv("Data_collection", "Sigfox")
Config_collection = os.getenv("Config_collection", "Config")

# initialize firebase sdk
CREDENTIALS = credentials.ApplicationDefault()
default_app = (
    initialize_app(CREDENTIALS, {"projectId": PROJECT_NAME})
    if ENV == "prod"
    # local Json
    else initialize_app(credentials.Certificate("local/nektiu-db.json"))
)


FIRESTORE_CLIENT = firestore.client()

data_root = FIRESTORE_CLIENT.collection(Data_collection)
Config_root = FIRESTORE_CLIENT.collection(Config_collection)
