import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json


def handshake(r_user_id: int) -> bool:
    """
    take in user id from Reminders app to sync with a user id in Contacts app
    need to log in to Contacts app with correct username and password
    if either `r_user_id` or `c_user_id` exists in `handshake_db`,
    function returns False.
    :param: r_user_id: provided by Reminders app
    :return: True/False
    """
    # refer to the credential key (json file)
    cred = credentials.Certificate(
        "/Users/ginwooklee_air/Library/CloudStorage/Box-Box/6_Winter23/CS361/contactMgmtPy"
        "/microservices/contactsmgmt-8647c-firebase-adminsdk-8c4vb-12ede2dd14.json"
    )

    # initialize `firebase_admin`
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://contactsmgmt-8647c-default-rtdb.firebaseio.com/"
    })

    # confirm `r_user_id` is not synced yet
    handshake_fb = db.reference('handshake_db').get()
    if handshake_fb is not None:
        for key in handshake_fb.keys():
            if handshake_fb[key]['r_user_id'] == r_user_id:
                print(f"user id [{r_user_id}] for Reminders app is "
                      f"already synced with user id [{handshake_fb[key]['c_user_id']}] "
                      f"of Contacts app.\n")
                return False

    # upload the latest `contacts_db.json` to firebase realtime database
    with open('./contacts_db.json', 'r') as r_contacts:
        contacts_db: list = json.load(r_contacts)
    db.reference('contacts_mgmt').child('contacts_db').set(contacts_db)

    # login to Contacts app
    username: str = input("Enter username: ")
    password: str = input("Enter password: ")

    # get the latest login profiles
    login_fb = db.reference('contacts_mgmt').child('login_db').get()

    # find matching user profile in Contacts app
    c_user_id: None or int = None
    for c_user in login_fb:
        if c_user['username'] == username and c_user['password'] == password:
            c_user_id = c_user['user_id']
            break

    # no user profile found in Contacts app
    if c_user_id is None:
        print(f"username: [{username}] and password [{password}] "
              f"didn't match with a user profile in Contacts app.\n")
        return False

    # confirm `c_user_id` is not synced yet
    if handshake_fb is not None:
        for key in handshake_fb.keys():
            if handshake_fb[key]['c_user_id'] == c_user_id:
                print(f"user id [{c_user_id}] for Contacts app is "
                      f"already synced with user id [{handshake_fb[key]['r_user_id']}] "
                      f"of Reminders app.\n")
                return False

    # update `handshake_db`
    db.reference('handshake_db').push({
        'c_user_id': c_user_id, 'r_user_id': r_user_id
    })
    print(f"Reminders app user id [{r_user_id}] "
          f"synced with Contacts app user id [{c_user_id}].\n")
    return True


if __name__ == '__main__':
    while True:
        print("handshake microservice is running...\n")
        # TODO: feed `reminder_id` from Reminders app
        request_from_reminder: int = int(input("Enter user id of Reminders app: "))
        is_synced: bool = handshake(request_from_reminder)
