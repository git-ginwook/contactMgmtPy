import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
# refer to the credential key (json file)
# TODO: update certificate JSON
cred = credentials.Certificate(
    "/Users/ginwooklee_air/Library/CloudStorage/Box-Box/6_Winter23/CS361/contactMgmtPy"
    "/microservices/contactsmgmt-8647c-firebase-adminsdk-8c4vb-12ede2dd14.json"
)

# initialize `firebase_admin`
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://contactsmgmt-8647c-default-rtdb.firebaseio.com/"
})


def handshake_ms(r_user_id: int, username: str, password: str) -> bool:
    """
    take in a user id from Reminders app to sync with a user id in Contacts app
    need to log in to Contacts app with correct username and password
    if either `r_user_id` or `c_user_id` exists in `handshake_db`,
    function returns False.
    Otherwise, returns True.
    :param r_user_id: provided by Reminders app
    :param username: provided by Reminders app
    :param password: provided by Reminders app
    :return: True/False
    """
    # get `handshake_db`
    handshake_fb: dict = json.loads(
        json.dumps(
            db.reference('handshake_db').get()
        )
    )

    # confirm `r_user_id` is not synced yet
    for key in handshake_fb.keys():
        if handshake_fb[key]['r_user_id'] == r_user_id:
            print("Return FALSE: "
                  f"user id [{r_user_id}] for Reminders app is "
                  f"already synced with user id [{handshake_fb[key]['c_user_id']}] "
                  f"of Contacts app.\n")
            return False

    # get the latest login profiles
    login_fb = json.loads(
        json.dumps
        (db.reference('contacts_mgmt').child('login_db').get()
         )
    )

    # find matching user profile in Contacts app
    c_user_id: None or int = None
    for c_user in login_fb.values():
        if c_user['username'] == username and c_user['password'] == password:
            c_user_id = c_user['user_id']
            break

    # no user profile found in Contacts app
    if c_user_id is None:
        print(f"username [{username}] and password [{password}] "
              "didn't match with a user profile in Contacts app.\n")
        return False

    # confirm `c_user_id` is not synced yet
    for key in handshake_fb.keys():
        if handshake_fb[key]['c_user_id'] == c_user_id:
            print("Return FALSE: "
                  f"user id [{c_user_id}] for Contacts app is "
                  f"already synced with user id [{handshake_fb[key]['r_user_id']}] "
                  "of Reminders app.\n")
            return False

    # update `handshake_db`
    db.reference('handshake_db').push({
        'c_user_id': c_user_id, 'r_user_id': r_user_id
    })
    print("Return TRUE: "
          f"Reminders app user id [{r_user_id}] "
          f"synced with Contacts app user id [{c_user_id}].\n")
    return True


if __name__ == '__main__':
    print("handshake microservice module")
