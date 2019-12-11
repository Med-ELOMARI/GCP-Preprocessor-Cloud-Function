import os

from firebase_admin import credentials, initialize_app, firestore
from google.auth.exceptions import DefaultCredentialsError


class Config:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "nektiu-4280d")
    Data_collection = os.getenv("Data_collection", "Sigfox")
    Config_collection = os.getenv("Config_collection", "Config")


class Tests(Config):
    # No need for firebase ... or inits
    pass


class Development(Config):
    if os.getenv("ENV", "dev") == "dev":
        default_app = initialize_app(credentials.Certificate("local/nektiu-db.json"))
        # initialize firebase sdk
        FIRESTORE_CLIENT = firestore.client()


class Production(Config):
    if os.getenv("ENV", "dev") == "prod":
        default_app = initialize_app(credentials.ApplicationDefault(), {"projectId": Config.PROJECT_NAME})
        # initialize firebase sdk
        try:
            FIRESTORE_CLIENT = firestore.client()
        except DefaultCredentialsError:
            print("Could not automatically determine credentials , Run the function on GCP not locally or switch to "
                  "ENV=dev")


configs = {"prod": Production, "dev": Development, "test": Tests}

# Config selection by ENV

config = configs[os.getenv("ENV", "dev")]
try:
    data_root = config.FIRESTORE_CLIENT.collection(Config.Data_collection)
    Config_root = config.FIRESTORE_CLIENT.collection(Config.Config_collection)
except AttributeError:
    # Passsing silently for Tests Class
    pass
