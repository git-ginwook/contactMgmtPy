import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(
    "/Users/ginwooklee_air/Library/CloudStorage/Box-Box/6_Winter23/CS361/contactMgmtPy"
    "/contactsmgmt-8647c-firebase-adminsdk-8c4vb-12ede2dd14.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://contactsmgmt-8647c-default-rtdb.firebaseio.com/"
})


# create
db.reference('contacts_mgmt').child('login').child('0').set({
    "user_id": 0,
    "username": "admin",
    "password": "1234",
    "last_user_id": 1
})
db.reference('contacts_mgmt').child('login').child('1').set({
    "user_id": 1,
    "username": "testUser",
    "password": "1234A*sk",
    "last_user_id": 1
})
db.reference('contacts_mgmt').child('contacts').child('0').set({
    "user_id": 0,
    "last_contact": 0,
    "contacts": [
        {
            "contact_id": 0,
            "f_name": "GinWook",
            "l_name": "Lee",
            "m_name": "",
            "phone": "404-983-5707",
            "email": "leeginw@oregonstate.edu",
            "address": "",
            "homepage": "",
            "company": "HP, Inc.",
            "department": "",
            "title": "big data engineer",
            "work phone": "",
            "work address": "",
            "memo": "this is me.",
            "reminder_1": "",
            "reminder_2": "",
            "reminder_3": "",
            "reminder_4": "",
            "reminder_5": ""
        }
    ]
})

# read
print(db.reference('contacts_mgmt').child('login').child('1').get())

# update
db.reference('contacts_mgmt').child('contacts').child('0').child('contacts').child('0').update({
    "memo": "using firebase realtime database"
})

# delete
db.reference('contacts_mgmt').child('login').child('1').child('last_user_id').delete()
