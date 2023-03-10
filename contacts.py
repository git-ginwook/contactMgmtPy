from firebase_admin import db
import json
import csv
import reminders_middleware


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

        # [0] log out
        if action == 0:
            return False
        # [1] create a contact
        elif action == 1:
            create_contact(user_pos)
            continue
        # [2] view a contact detail
        elif action == 2:
            contact_pos, contact_id = val_contact_id(user_pos)
            # GET request from Reminders app on `user_id`
            reminders: list = reminders_middleware.getreminders(user_id)
            # check if synced
            if type(reminders) is str:
                read_contact(user_pos, contact_pos, contact_id, None)
            else:
                read_contact(user_pos, contact_pos, contact_id, reminders)
            continue
        # [3] update a contact
        elif action == 3:
            contact_pos, contact_id = val_contact_id(user_pos)
            update_contact(user_pos, contact_pos, contact_id)
            continue
        # [4] delete a contact
        elif action == 4:
            contact_pos, contact_id = val_contact_id(user_pos)
            delete_contact(user_pos, contact_pos, contact_id)
            continue
        # [5] sync account with Reminders App
        elif action == 5:
            sync_accounts(user_id)
            continue
        # [6] download all contacts
        elif action == 6:
            download_all(contacts)
            continue
        # [7] search
        elif action == 7:
            search(contacts)
            continue

        return True


def read_contact(user_pos: str, contact_pos: str, contact_id: int, reminders: list or None) -> None:
    """
    read and display a select contact
    :param: user_pos: from view_all()
    :param: contact_pos: from val_contact_id()
    :param: contact_id: from val_contact_id()
    :param: reminders: Reminders list called from Reminders App
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

    # return if not synced
    if reminders is None:
        print("\n")
        return

    #  continue if synced
    i: int = 1
    for task in reminders:
        # TODO: re-confirm new attribute names
        if task['contact_id'] == str(contact_id):
            print(f"    reminder_{i}: {task['name']} by {task['date']} {task['time']}")
            i += 1
    print("\n")

    return


def update_contact(user_pos: str, contact_pos: str, contact_id: int) -> None:
    """
    update values of select attribute(s) for a select contact
    :param: user_pos: from view_all()
    :param: contact_pos: from val_contact_id()
    :param: contact_id: from val_contact_id()
    :return: None
    """
    # display select contact details
    read_contact(user_pos, contact_pos, contact_id, None)

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
    :param: user_pos: from account login
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
        "memo": input("Memo: ").strip()
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


def delete_contact(user_pos: str, contact_pos: str, contact_id: int) -> None:
    """
    delete a select contact
    :param: user_pos: from view_all()
    :param: contact_pos: from val_contact_id()
    :param: contact_id: from val_contact_id()
    :return: None
    """
    contact: dict = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('contacts_db').
            child(user_pos).child('contacts').child(contact_pos).get()
        )
    )

    # prevent user from deleting self profile
    if contact['contact_id'] == 0:
        print("You cannot delete your self profile.\n")
        return

    # show select contact profile
    read_contact(user_pos, contact_pos, contact_id, None)

    # confirm user action
    is_accept = input("Enter 1 to delete or 2 to cancel: ")
    if is_accept != "1":
        return

    # delete from `contacts_db`
    db.reference('contacts_mgmt').child('contacts_db').\
        child(user_pos).child('contacts').child(contact_pos).delete()

    return


def create_self(user_id: int) -> None:
    """
    user creates a self profile when logging in for the first time
    :param: user_id: from account login
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
        "memo": input("Memo: ").strip()
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
    :param: user_id: from account login
    :return: None
    """
    # locate `user_id`
    contacts_db: dict = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('contacts_db').get()
        )
    )
    for key, val in contacts_db.items():
        if val['user_id'] == user_id:
            # delete all contacts associated with `user_id`
            db.reference('contacts_mgmt').child('contacts_db').child(key).delete()
            break

    print(f"All contacts deleted.\n")
    return


def sync_accounts(user_id: int) -> None:
    """
    invoke handshake microservice to sync two accounts
    between Contacts App and Reminders App
    :param: user_id: from view_all()
    :return: None
    """
    print("To sync the Contacts App account with your Reminders App account, "
          "you have to login to the Reminders App using email and password.\n"
          "You only need to synchronize once.\n")
    # get user inputs to access Reminders App
    email: str = input("Enter email: ")
    password: str = input("Enter password: ")

    # call handshake microservice to connect to Reminders App
    if reminders_middleware.handshake(email, password, user_id) != "Server Error":
        print("Successful handshake! Now you can access your reminders from Contacts App!\n")
    else:
        print("Unsuccessful handshake... Please try again.\n")

    return


def download_all(contacts: dict) -> None:
    """
    write a csv file containing all contacts data of a user

    if a csv file with the same filename already exists,
    data will be overwritten.

    :param: contacts: from view_all()
    :return: None
    """
    # reformat contacts data into dict within list
    contacts_dict = []
    for contact in contacts.values():
        contacts_dict.append(contact)

    # list column names
    field_names = ['contact_id',
                   'f_name', 'm_name', 'l_name',
                   'phone', 'email', 'address', 'homepage',
                   'company', 'department', 'title',
                   'work phone', 'work address',
                   'memo']

    # user input for filename
    filename = input("Enter filename: ")

    # write/overwrite contacts data to a csv file
    with open(f'{filename}.csv', "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(contacts_dict)

    return


def search(contacts: dict) -> None:
    """
    search for matching `attribute` and `value`
    - search for substring
    - search ignores case sensitivity

    :param: contacts: from view_all()
    :return: None
    """
    # display attribute names
    print("[List of attribute names]")
    for name in list(list(contacts.values())[0].keys()):
        print(f'    {name}')
    print('\n')

    # user search input
    attribute = input("Enter attribute name: ")
    value = input("Enter search value: ")

    for contact in contacts.values():
        # convert value to integer type for `contact_id`
        if attribute == 'contact_id':
            if contact['contact_id'] == int(value):
                print(contact)

        # search for contact that contains `value` (ignoring case)
        elif value.lower() in contact[f'{attribute}'].lower():
            print(contact)

    print('\n')

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
                "What would you like to do with your contacts? [0 ~ 7]\n"
                "    [0] log out\n"
                "    [1] create a contact\n"
                "    [2] view a contact detail\n"
                "    [3] update a contact\n"
                "    [4] delete a contact\n"
                "    [5] sync account with Reminders App\n"
                "    [6] download all contacts\n"
                "    [7] search\n"
            )
            action = int(action)
        except ValueError as val:
            print(f"{val}. Please enter an integer [0 ~ 7].")
            continue
        except EOFError:
            raise EOFError("[Exit Contact Management App]")
        else:
            if 0 <= action <= 7:
                print(f"Your contact action: [{action}]")
                return action
            else:
                continue


def val_contact_id(user_pos: str) -> str and int:
    """
    validate contact id
    - check if user input is an integer
    - check if contact id exists in the database
    :param: user_pos: from account login
    :return: validated contact_id and its Firebase key
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
            contact_id = input("Enter contact_id: ")
            contact_id = int(contact_id)
        except ValueError as val:
            print(f"{val}. Please enter an integer.")
            continue
        except EOFError:
            raise EOFError("[Exit Contact Management App]")
        else:
            for key, val in contacts.items():
                if val['contact_id'] == contact_id:
                    return key, contact_id

            print(f"Contact id [{contact_id}] doesn't exist. "
                  "Please enter a valid contact id.")


def val_req_attr(req_attr: str) -> str:
    """
    validate whether a required attribute is empty
    :param: req_attr: contact attribute name
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
    print("contacts module")
