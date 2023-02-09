from firebase_admin import db
import json

contacts_fp: str = './contacts_db.json'
CONTACTS_ADMIN = '-NNlh7tcSVNFgf1HRqa1'


def view_all(user_id: int) -> bool:
    """
    view all contacts for `user_id`
    if logging in for the first time, user should complete self profile
    :param: user_id: from account login
    :return: True/False
    """
    while True:
        user_pos: None or str = None

        # identify the position of contacts profile for `user_id`
        contacts_db: dict = json.loads(
            json.dumps(
                db.reference('contacts_mgmt').child('contacts_db').get()
            )
        )
        for key, val in contacts_db.items():
            if val['user_id'] == user_id:
                user_pos = key
                break

        # check if first time logging in
        if user_pos is None:
            # create self profile
            create_self(user_id)
            return True

        # read all contacts related to `user_id`
        print("[ALL CONTACTS]")
        contacts: dict = json.loads(
            json.dumps(
                db.reference('contacts_mgmt').child('contacts_db').child(user_pos).child('contacts').get()
            )
        )
        for contact in contacts.values():
            print(f"ID: {contact['contact_id']} | "
                  f"Name: {contact['f_name']} {contact['l_name']}")
        print("\n")

        # choose action
        action: int = choose_action()

        if action == 0:
            return False
        elif action == 1:
            create_contact(user_pos)
            continue
        elif action == 2:
            read_contact(user_pos, val_contact_id(user_pos))
            continue
        elif action == 3:
            update_contact(user_pos, val_contact_id(user_pos))
            continue
        elif action == 4:
            delete_contact(user_id, val_contact_id(user_pos))
            continue
        return True


def read_contact(user_pos: str, contact_pos: str) -> str:
    """
    read and display a select contact
    :param user_pos: from view_all()
    :param contact_pos: from val_contact_id()
    :return: contact position
    """
    # get contact details
    contact: dict = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('contacts_db').
            child(user_pos).child('contacts').child(contact_pos).get()
        )
    )

    # display contact details
    for key, val in contact.items():
        print(f"    {key}: {val}")
    print("\n")

    return contact_pos


def update_contact(user_pos: str, contact_pos: str) -> None:
    """
    update values of select attribute(s) for a select contact
    :param user_pos: from view_all()
    :param contact_pos: from val_contact_id()
    :return: None
    """
    # display select contact details
    read_contact(user_pos, contact_pos)

    # get contact details
    contact: dict = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('contacts_db').
            child(user_pos).child('contacts').child(contact_pos).get()
        )
    )
    # get user input to update contact
    while True:
        try:
            attr = input("Enter an attribute to change: ")
            cur_val: str = contact[attr]
            new_val = input(f"Enter new value for [{attr}]: ").strip()
        except KeyError as key:
            print(f"{key}. Please enter a valid attribute.\n")
            continue
        except EOFError:
            raise EOFError("[Exit Contact Management App]")
        else:
            if attr == "contact_id":
                print("You cannot change [contact_id].\n")
                continue
            elif attr[:8] == "reminder":
                print("You cannot change [reminder_#].\n")
                continue
            elif cur_val == new_val:
                print("You entered the same value as the current one."
                      "Please try again.\n")
                continue
            else:
                contact[attr] = new_val

            go_stop = input("Enter 1 to continue change or 2 to stop: ")
            if go_stop == "1":
                continue
            elif go_stop == "2":
                break
            else:
                print("Invalid option. Please enter 1 or 2.\n")
                break

    # confirm user action
    is_accept = input("Enter 1 to accept the change(s) or 2 to cancel: ")
    if is_accept != "1":
        print("Cancel al the change(s) made.\n")
        return

    # update contact details
    db.reference('contacts_mgmt').child('contacts_db').\
        child(user_pos).child('contacts').\
        child(contact_pos).update(contact)
    print("Thanks for the update.\n")
    return


def create_contact(user_pos: str) -> None:
    """
    create a new contact profile
    :param user_pos: from account login
    :return: None
    """
    contacts_attr: dict = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('contacts_db').child(user_pos).get()
        )
    )
    new_contact_id: int = contacts_attr['last_contact_id'] + 1

    # create `contact_profile`
    contact_profile: dict = {
        "contact_id": new_contact_id,
        "f_name": val_req_attr("f_name"),
        "l_name": val_req_attr("l_name"),
        "m_name": input("Middle name: ").strip(),
        "phone": input("Phone number: ").strip(),
        "email": input("Email address: ").strip(),
        "address": input("Home address: ").strip(),
        "homepage": input("Homepage: ").strip(),
        "company": input("Company: ").strip(),
        "department": input("Department: ").strip(),
        "title": input("Title: ").strip(),
        "work phone": input("Work phone: ").strip(),
        "work address": input("Work address: ").strip(),
        "memo": input("Memo: ").strip(),
        # TODO: GET request from Reminders app
        "reminder_1": "",  # from reminders app
        "reminder_2": "",  # from reminders app
        "reminder_3": "",  # from reminders app
        "reminder_4": "",  # from reminders app
        "reminder_5": ""  # from reminders app
    }

    # confirm user action
    is_accept = input("Enter 1 to accept the change or 2 to cancel: ")
    if is_accept != "1":
        return

    # # append `contact_profile`
    db.reference('contacts_mgmt').child('contacts_db').child(user_pos).child('contacts').push(contact_profile)

    # # increment `last_contact_id`
    db.reference('contacts_mgmt').child('contacts_db').child(user_pos).update({'last_contact_id': new_contact_id})

    # ask for the subsequent action
    go_stop: str = input("Enter 1 to create another or 2 to stop: ")
    if go_stop == "1":
        create_contact(user_pos)
    print("\n")
    return


def delete_contact(user_id: int, contact_id: int) -> None:
    """
    delete a select contact
    :param user_id: from account login
    :param contact_id: from view_all()
    :return: None
    """
    # prevent user from deleting self profile
    if contact_id == 0:
        print("You cannot delete your self profile.\n")
        return

    # show select contact profile
    contacts_db, contact, pos_u, pos_c = read_contact(user_id, contact_id)

    # confirm user action
    is_accept = input("Enter 1 to delete or 2 to cancel: ")
    if is_accept != "1":
        return

    # delete from `contacts_db`
    contacts_db[pos_u]["contacts"].pop(pos_c)

    # apply change(s) to `contacts_db.json`
    with open(contacts_fp, "w") as w_contacts:
        json.dump(contacts_db, w_contacts, indent=4)
    print(f"contact_id: {contact_id} removed successfully.\n")

    return


def create_self(user_id: int) -> None:
    """
    user creates a self profile when logging in for the first time
    :param user_id: from account login
    :return: None
    """
    user_pos: None or str = None

    print("Thanks for creating your user profile "
          "and logging in for the first time!\n")

    # complete self profile
    print("Please fill out your profile before "
          "adding other contacts!\n")
    self_profile: dict = {
        "contact_id": 0,
        "f_name": val_req_attr("f_name"),
        "l_name": val_req_attr("l_name"),
        "m_name": input("Middle name: ").strip(),
        "phone": input("Phone number: ").strip(),
        "email": input("Email address: ").strip(),
        "address": input("Home address: ").strip(),
        "homepage": input("Homepage: ").strip(),
        "company": input("Company: ").strip(),
        "department": input("Department: ").strip(),
        "title": input("Title: ").strip(),
        "work phone": input("Work phone: ").strip(),
        "work address": input("Work address: ").strip(),
        "memo": input("Memo: ").strip(),
        # TODO: GET request from Reminders app
        "reminder_1": "",  # from reminders app
        "reminder_2": "",  # from reminders app
        "reminder_3": "",  # from reminders app
        "reminder_4": "",  # from reminders app
        "reminder_5": ""  # from reminders app
    }

    # confirm user action
    is_accept = input("Enter 1 to accept the change or 2 to cancel: ")
    if is_accept != "1":
        return

    # create a new contacts profile for `user_id`
    db.reference('contacts_mgmt').child('contacts_db').push({
        'user_id': user_id,
        'last_contact_id': 0,
        'contacts': None
    })

    # identify the position of new contacts profile
    contacts_db: dict = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('contacts_db').get()
        )
    )
    for key, val in contacts_db.items():
        if val['user_id'] == user_id:
            user_pos = key
            break

    # update self profile to the new contacts profile
    db.reference('contacts_mgmt').child('contacts_db').child(user_pos).child('contacts').push(self_profile)
    print("Thanks for completing your profile.\n")
    return


def delete_all(user_id: int) -> None:
    """
    delete all contacts associated with `user_id`
    :param user_id: from account login
    :return: None
    """
    # open `contacts_db.json`
    with open(contacts_fp, "r") as r_contacts:
        contacts_db: list = json.load(r_contacts)

    # locate `user_id`
    pos_u: None or int = None
    for idx, user in enumerate(contacts_db):
        if user["user_id"] == user_id:
            pos_u = idx
            break

    # delete all contacts associated with `user_id`
    contacts_db.pop(pos_u)

    # update `contacts_db.json`
    with open(contacts_fp, "w") as w_contacts:
        json.dump(contacts_db, w_contacts, indent=4)
    print(f"All contacts deleted.\n")

    return


def choose_action() -> int:
    """
    user chooses contact action
    :return: valid option number
    """
    # choose contact action
    while True:
        try:
            action = input(
                "What would you like to do with your contacts? [0 ~ 4]\n"
                "    [0] log out\n"
                "    [1] create a contact\n"
                "    [2] view a contact detail\n"
                "    [3] update a contact\n"
                "    [4] delete a contact\n"
            )
            action = int(action)
        except ValueError as val:
            print(f"{val}. Please enter an integer [0 ~ 4].")
            continue
        except EOFError:
            raise EOFError("[Exit Contact Management App]")
        else:
            if 0 <= action <= 4:
                print(f"Your contact action: [{action}]")
                return action
            else:
                continue


def val_contact_id(user_pos: str) -> str:
    """
    validate contact id
    - check if user input is an integer
    - check if contact id exists in the database
    :param user_pos: from account login
    :return: validated contact_id
    """
    # get user's contacts
    contacts: dict = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('contacts_db').child(user_pos).child('contacts').get()
        )
    )

    # user input validation for `contact_id`
    while True:
        try:
            contact_id = input("Enter contact_id for details: ")
            contact_id = int(contact_id)
        except ValueError as val:
            print(f"{val}. Please enter an integer.")
            continue
        except EOFError:
            raise EOFError("[Exit Contact Management App]")
        else:
            for key, val in contacts.items():
                if val['contact_id'] == contact_id:
                    return key

            print(f"Contact id [{contact_id}] doesn't exist. "
                  "Please enter a valid contact id.")


def val_req_attr(req_attr: str) -> str:
    """
    validate whether a required attribute is empty
    :param req_attr: contact attribute name
    :return: valid user input
    """
    user_input: str = ""
    if req_attr == "f_name":
        while True:
            user_input = input("First name (required): ").strip()
            if user_input == "":
                print(f"{req_attr} cannot be empty.")
                continue
            break
    elif req_attr == "l_name":
        while True:
            user_input = input("Last name (required): ").strip()
            if user_input == "":
                print(f"{req_attr} cannot be empty.")
                continue
            break

    return user_input


if __name__ == '__main__':
    print("contact list module")
