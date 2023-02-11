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


def contacts_ms(r_user_id: int) -> dict or bool:
    """

    :param r_user_id: provided by Reminders app
    :return:
    - if succeeded, contacts info associated with `r_user_id`
    - if failed, return False
    """
    # get `handshake_db`
    handshake_fb: dict = json.loads(
        json.dumps(
            db.reference('handshake_db').get()
        )
    )

    # find `c_user_id` synced with `r_user_Id`
    c_user_id: None or int = None
    for val in handshake_fb.values():
        if val['r_user_id'] == r_user_id:
            c_user_id = val['c_user_id']
            break

    # return False if `r_user_id` is not synced yet
    if c_user_id is None:
        print("Return False: "
              f"r_user_id [{r_user_id}] is not synced with Contacts app. "
              "Please handshake before accessing contacts info.\n")
        return False

    # get `contacts_db`
    contacts_fb: dict = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('contacts_db').get()
        )
    )

    # get key for `c_user_id` from `contacts_db`
    c_key: None or int = None
    for key, val in contacts_fb.items():
        if val['user_id'] == c_user_id:
            c_key = key
            break

    # return False if `c_user_id` doesn't exist (i.e., deleted) in Contacts app
    if c_key is None:
        print("Return False: "
              f"c_user_id [{c_user_id}] associated with r_user_id [{r_user_id}] "
              f"no longer exists in Contacts app.\n")
        return False

    # get `contact`
    contacts_db: dict = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('contacts_db').
            child(c_key).child('contacts').get()
        )
    )

    # make a dictionary of requested attributes
    contacts_dict: dict = dict({'contacts': []})
    for val in contacts_db.values():
        contacts_dict['contacts'].append({
            'contact_id': val['contact_id'],
            'f_name': val['f_name'],
            'l_name': val['l_name']
        })

    return contacts_dict


if __name__ == '__main__':
    while True:
        print("contacts microservice is running...\n")
        # TODO: feed `user_id` from zmq
        user_id: int = int(input("Enter user id of Reminders app: "))
        res_contacts: dict = contacts_ms(user_id)
