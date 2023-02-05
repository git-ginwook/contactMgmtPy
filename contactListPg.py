import json

contacts_fp: str = './contacts_db.json'


def view_all(user_id: int) -> bool:
    """
    view all contacts for `user_id`
    if logging in for the first time, user should complete self profile
    :param: user_id: from account login
    :return: True/False
    """
    while True:
        pos: None or int = None

        # open `contacts_db.json`
        with open(contacts_fp, "r") as r_contacts:
            contacts_db: list = json.load(r_contacts)

        # check if first time logging in
        for idx, user in enumerate(contacts_db):
            if user["user_id"] == user_id:
                pos = idx
                break

        # first time logging in
        if pos is None:
            # create self profile
            create_self(contacts_db, user_id)
            return True

        print("[ALL CONTACTS]")
        # read all contacts related to `user_id`
        for contact in contacts_db[pos]["contacts"]:
            print(f"    ID: {contact['contact_id']} | "
                  f"Name: {contact['f_name']} {contact['l_name']}")
        print("\n")

        # choose action
        action: int = choose_action()

        if action == 0:
            return False
        elif action == 1:
            create_contact(user_id)
            continue
        elif action == 2:
            read_contact(user_id, val_contact_id(user_id))
            continue
        elif action == 3:
            update_contact(user_id, val_contact_id(user_id))
            continue
        elif action == 4:
            delete_contact(user_id, val_contact_id(user_id))
            continue

        return True


def read_contact(user_id: int, contact_id: int) -> \
        list and dict and int and int:
    """
    read and display a select contact
    :param user_id: from account login
    :param contact_id: from view_all()
    :return: contacts_db, select contact, user position, contact position
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

    # locate `contact_id`
    pos_c: None or int = None
    for idx, contact in enumerate(contacts_db[pos_u]["contacts"]):
        if contact["contact_id"] == contact_id:
            pos_c = idx
            break

    # show contact info
    contact: dict = contacts_db[pos_u]["contacts"][pos_c]
    for attr in contact:
        print(f"    {attr}: {contact[attr]}")
    print("\n")

    return contacts_db, contact, pos_u, pos_c


def update_contact(user_id: int, contact_id: int) -> None:
    """
    update values of select attribute(s) for a select contact
    :param user_id: from account login
    :param contact_id: from view_all()
    :return: None
    """
    # show select contact profile
    contacts_db, contact, pos_u, pos_c = read_contact(user_id, contact_id)

    # get user input to update contact
    while True:
        try:
            attr: str = input("Enter an attribute to change: ")
            key_test: str = contact[attr]
            change: str = input(f"Enter new value for {attr}: ").strip()
        except KeyError as key:
            print(f"{key}. Please enter a valid attribute.")
            continue
        except EOFError:
            raise EOFError("[Exit Contact Management App]")
        else:
            if attr == "contact_id":
                print("You cannot change contact_id.")
                continue
            else:
                if key_test != change:
                    contact[attr] = change

            go_stop = input("Enter 1 to continue change or 2 to stop: ")
            if go_stop == "1":
                continue
            elif go_stop == "2":
                break
            else:
                print("Invalid option. Please enter 1 or 2.")
                break

    # confirm user action
    is_accept = input("Enter 1 to accept the change or 2 to cancel: ")
    if is_accept != "1":
        print("Cancel al the change(s) made.\n")
        return

    # update `contacts_db.json`
    with open(contacts_fp, "w") as w_contacts:
        json.dump(contacts_db, w_contacts, indent=4)
    print("Thanks for the update.\n")

    return


def create_contact(user_id: int) -> None:
    """
    create a new contact profile
    :param user_id: from account login
    :return: None
    """
    # read `contacts_db.json`
    with open(contacts_fp, "r") as r_contacts:
        contacts_db: list = json.load(r_contacts)

    # locate `user_id`
    pos_u: None or int = None
    for idx, user in enumerate(contacts_db):
        if user["user_id"] == user_id:
            pos_u = idx
            break

    # create `contact_profile`
    contact_profile: dict = {
        "contact_id": contacts_db[pos_u]["last_contact"] + 1,
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

    # append `contact_profile`
    contacts_db[pos_u]["contacts"].append(contact_profile)

    # increment `last_contact`
    contacts_db[pos_u]["last_contact"] += 1

    # write new `contact_profile` to `contacts_db.json`
    with open(contacts_fp, "w") as w_contacts:
        json.dump(contacts_db, w_contacts, indent=4)
    print("Thanks for creating a new contact profile.\n")

    # ask for the subsequent action
    go_stop: str = input("Enter 1 to create another or 2 to stop: ")
    if go_stop == "1":
        create_contact(user_id)

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


def create_self(contacts_db: list, user_id: int) -> None:
    """
    user creates a self profile when logging in for the first time
    :param contacts_db: from view_all()
    :param user_id: from account login
    :return: None
    """
    print("Thanks for creating your user profile "
          "and logging in for the first time!\n")

    # complete self profile
    print("Please fill out your profile before "
          "adding other contacts!\n")
    self_profile: dict = {
        "user_id": user_id,
        "last_contact": 0,
        "contacts": [
            {
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
        ]
    }

    # confirm user action
    is_accept = input("Enter 1 to accept the change or 2 to cancel: ")
    if is_accept != "1":
        return

    # write to `contacts_db.json`
    contacts_db.append(self_profile)
    with open(contacts_fp, "w") as w_contacts:
        json.dump(contacts_db, w_contacts, indent=4)
    print("Thanks for completing your profile.\n")
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


def val_contact_id(user_id: int) -> int:
    """
    validate contact id
    - check if user input is an integer
    - check if contact id exists in the database
    :param user_id: from account login
    :return: validated contact_id
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

    # list up `contact_id`
    id_list: list = []
    for contact in contacts_db[pos_u]["contacts"]:
        id_list.append(contact["contact_id"])

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
            if contact_id not in id_list:
                print(f"Contact id [{contact_id}] doesn't exist. "
                      "Please enter a valid contact id.")
                continue

            return contact_id


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
