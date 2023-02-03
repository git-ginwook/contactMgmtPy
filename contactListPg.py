import json

contacts_fp: str = './contacts_db.json'


def view_contact(user_id: int) -> bool:
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
    for idx, contact in enumerate(contacts_db):
        if contact["user_id"] == user_id:
            pos = idx

    # first time logging in
    if pos is None:
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
        return True

    # read all contacts related to `user_id`
    for contact in contacts_db[pos]["contacts"]:
        print(
            "ID: ", contact["contact_id"], "\t",
            "Full name: ", contact["f_name"], contact["l_name"]
        )

    return False


def update_contact():
    pass


def create_contact():
    pass


def delete_contact():
    pass


if __name__ == '__main__':
    print("contact list module")
