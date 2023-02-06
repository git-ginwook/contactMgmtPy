import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

# refer to the credential key (json file)
cred = credentials.Certificate(
    "/Users/ginwooklee_air/Library/CloudStorage/Box-Box/6_Winter23/CS361/contactMgmtPy"
    "/contactsmgmt-8647c-firebase-adminsdk-8c4vb-12ede2dd14.json"
)

# initialize `firebase_admin`
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://contactsmgmt-8647c-default-rtdb.firebaseio.com/"
})

# upload the latest `login_db.json` to firebase realtime database
with open('./login_db.json', 'r') as r_login:
    login_db: list = json.load(r_login)
db.reference('contacts_mgmt').child('login').set(login_db)

# upload the latest `contacts_db.json` to firebase realtime database
with open('./contacts_db.json', 'r') as r_contacts:
    contacts_db: list = json.load(r_contacts)
db.reference('contacts_mgmt').child('contacts').set(contacts_db)

