import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json


def handshake(r_user_id: int) -> bool:
    """

    :return: True/False
    """
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

    # login to Contacts app
    username: str = input("Enter username: ")
    password: str = input("Enter password: ")

    # get the latest login profiles
    login = db.reference('contacts_mgmt').child('login').get()

    # find matching user profile in Contacts app
    for c_user in login:
        if c_user['username'] == username and c_user['password'] == password:
            c_user_id = c_user['user_id']

            db.reference('handshake').push({
                'c_user_id': c_user_id, 'r_user_id': r_user_id
            })
            print(f"Reminders app user id [{r_user_id}] "
                  f"synced with Contacts app user id [{c_user_id}].\n")
            return True

    print(f"username: [{username}] and password [{password}] "
          f"didn't match with a user profile in Contacts app.")
    return False


if __name__ == '__main__':
    # TODO: need to take handshake request with r_user_id
    request_from_reminder = 0
    # TODO: need to return status as a response
    handshake(request_from_reminder)
