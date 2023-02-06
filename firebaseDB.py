import pyrebase

# Firebase >> ContactsMgmt >> Realtime Database
config = {
    "apiKey": "AIzaSyBXPj7Qrefizn2MjM0DZCHWHvVupZ32RLs",
    "authDomain": "contactsmgmt-8647c.firebaseapp.com",
    "projectId": "contactsmgmt-8647c",
    "storageBucket": "contactsmgmt-8647c.appspot.com",
    "messagingSenderId": "255155017412",
    "appId": "1:255155017412:web:9b3eb393ff1cd26ee11b91",
    "databaseURL": "https://console.firebase.google.com/"
                   "u/0/project/contactsmgmt-8647c/database/"
                   "contactsmgmt-8647c-default-rtdb/data/~2F"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

