import json

contacts_fp: str = './contacts_db.json'


def view_all(user_id: int) -> bool:
    """
    view all contacts for `user_id`

    if logging in for the first time, complete self profile

    :param: user_id: from account login
    :return: True/False
    """
    pos: None or int = None

    # open `contacts_db`
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

    while True:
        # read all contacts related to `user_id`
        for contact in contacts_db[pos]["contacts"]:
            print(f"    ID: {contact['contact_id']} | "
                  f"Full name: {contact['f_name']} {contact['l_name']}")
        print("\n")

        # choose action
        action: int = choose_action()

        if action == 0:
            return False
        elif action == 1:
            create_contact(user_id)
            continue
        elif action == 2:
            read_contact(
                user_id,
                int(input("Enter contact_id: "))
            )      # TODO: validate input
            continue
        elif action == 3:
            update_contact(
                user_id,
                int(input("Enter contact_id: "))
            )       # TODO: validate input
            continue
        elif action == 4:
            delete_contact(
                user_id,
                int(input("Enter contact_id: "))
            )       # TODO: validate input
            continue

        return True


def read_contact(user_id: int, contact_id: int) -> None:
    """
    read and display a select contact
    :param user_id: from account login
    :param contact_id: asd
    :return: None
    """
    # open `contacts_db`
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
        print(attr, ": ", contact[attr])
        print(f"    {attr}: {contact[attr]}")
    print("\n")

    return


def update_contact(user_id: int, contact_id: int) -> None:
    """
    update values of select attribute(s) for a select contact
    :param user_id: from account login
    :param contact_id:
    :return: None
    """
    # open `contacts_db`
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
        print(f"{attr}: {contact[attr]}")

    # get user input to update contact
    while True:
        try:
            attr: str = input("Enter an attribute to change: ")
            key_test: str = contact[attr]
            change: str = input(f"Enter new value for {attr}: ")
        except KeyError as key:
            print(f"{key}. Please enter a valid attribute.")
            continue
        except EOFError:
            raise EOFError("Exit Contact Management App")
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

    # update `contacts_db`
    with open(contacts_fp, "w") as w_contacts:
        json.dump(contacts_db, w_contacts, indent=4)
    print("Thanks for the update.\n")

    return


def create_contact(user_id: int) -> None:
    """

    :param user_id: from account login
    :return: None
    """


def delete_contact(user_id: int, contact_id: int) -> None:
    """

    :param user_id: from account login
    :param contact_id:
    :return:
    """


def create_self(contacts_db: list, user_id: int) -> None:
    """

    :param contacts_db:
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
                "f_name": input("First name (required): "),  # TODO: no empty check 1
                "l_name": input("Last name (required): "),  # TODO: no empty check 2
                "m_name": input("Middle name: "),
                "phone": input("Phone number: "),
                "email": input("Email address: "),
                "address": input("Home address: "),
                "homepage": input("Homepage: "),
                "company": input("Company: "),
                "department": input("Department: "),
                "title": input("Title: "),
                "work phone": input("Work phone: "),
                "work address": input("Work address: "),
                "memo": input("Memo: "),
                # TODO: GET request from Reminders app
                "reminder_1": "",  # from reminders app
                "reminder_2": "",  # from reminders app
                "reminder_3": "",  # from reminders app
                "reminder_4": "",  # from reminders app
                "reminder_5": ""  # from reminders app
            }
        ]
    }

    # write to `contacts_db`
    contacts_db.append(self_profile)
    with open(contacts_fp, "w") as w_contacts:
        json.dump(contacts_db, w_contacts, indent=4)
    print("Thanks for completing your profile.\n")


def choose_action() -> int:
    """

    :return:
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
            raise EOFError("Exit Contact Management App")
        else:
            if 0 <= action <= 4:
                print(f"Your contact action: [{action}]")
                return action
            else:
                continue


def val_contact_id() -> int:
    """
    validation:
    - check if user input is an integer
    - check if contact id exists in the database

    :return:
    """
    # TODO: validate contact id input


if __name__ == '__main__':
    print("contact list module")
