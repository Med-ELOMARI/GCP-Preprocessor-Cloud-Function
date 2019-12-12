import os

from firebase_admin import credentials, initialize_app, firestore
from google.auth.exceptions import DefaultCredentialsError

DEFAULT_PROJECT_NAME = "nektiu-4280d"
DEFAULT_DATA_collection_name = "Sigfox"
DEFAULT_CONFIG_collection_name = "Config"

class Config:
    PROJECT_NAME = os.getenv("PROJECT_NAME", DEFAULT_PROJECT_NAME)
    Data_collection = os.getenv("DATA_COLLECTION_NAME", DEFAULT_DATA_collection_name)
    Config_collection = os.getenv("CONFIG_COLLECTION_NAME", DEFAULT_CONFIG_collection_name)


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
