from firebase_admin import credentials, firestore, initialize_app

PROJECT_NAME = 'nektiu-4280d'

# initialize firebase sdk
CREDENTIALS = credentials.ApplicationDefault()
default_app = initialize_app(CREDENTIALS, {
    'projectId': PROJECT_NAME,
})
FIRESTORE_CLIENT = firestore.client()

data_root = FIRESTORE_CLIENT.collection("Sigfox")
Config_root = FIRESTORE_CLIENT.collection("Config")

