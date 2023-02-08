from firebase_admin import db
import json
# login admin key
LOGIN_ADMIN = "-NNlN7pcoRbhldry0ZYs"


def access_login() -> bool and dict:
    """
    login with username and password

    :return: True/False, user profile
    """
    attempt: int = 1
    max_attempt: int = 5

    print("Login with your username and password.")
    for i in range(attempt, max_attempt+1):
        try:
            # get user inputs
            username: str = input("Username: ")
            password: str = input("Password: ")

        except EOFError:
            raise EOFError("[Exit Contact Management App]")

        else:
            # convert collections object to dict
            login_db: dict = json.loads(
                json.dumps(
                    db.reference('contacts_mgmt').child('login_db').get()
                )
            )

            for profile in login_db.values():
                if profile["username"] == username and \
                        profile["password"] == password:
                    print("Login was successful!\n")
                    return True, profile

            if attempt < max_attempt:
                print("Username and password don't match - please try again. "
                      f"[{attempt}/{max_attempt}]")
                attempt += 1
                continue
            elif attempt == max_attempt:
                print("Too many wrong attempts. "
                      f"[{attempt}/{max_attempt}]\n")

            return False, None


def create_login() -> None:
    """
    create a user profile with username and password

    RULES:
    - username must be unique and less than 24 characters.
    - password must be between 8-12 characters.
    - password must have at least one special character: !@#$%^&*()-_+="
    - password must have at least one number.
    - password must have at least one uppercase.

    :return: None
    """
    print("Create username and password.")
    print("RULES:")
    print("    - username must be unique and less than 24 characters.")
    print("    - password must be between 8-12 characters.")
    print("    - password must have at least one special character: "
          "!@#$%^&*()-_+=")
    print("    - password must have at least one number.")
    print("    - password must have at least one uppercase.")

    # validate username
    username: str = input("Username: ")
    is_unique = val_username(username)
    if not is_unique:
        return

    # validate password
    password: str = input("Password: ")
    is_val = val_password(password)

    if not is_val:
        return

    # confirm user action
    while True:
        try:
            print("Are you sure you want to create your profile?")
            is_confirm = input("Please enter 1 for YES or 2 for NO: ")
            is_confirm = int(is_confirm)
        except ValueError as val:
            print(f"{val}. Please enter an integer [1 or 2].")
            continue
        except EOFError:
            raise EOFError("[Exit Contact Management App]")
        else:
            if is_confirm == 1:
                break
            elif is_confirm == 2:
                print("No new user file.\n")
                return
            else:
                print("Please enter an integer [1 or 2].")
                continue

    # convert collections object to dict
    login_db: dict = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('login_db').get()
        )
    )

    # increment `last_user_id`
    db.reference('contacts_mgmt').child('login_db').child(LOGIN_ADMIN).update({
        'last_user_id': login_db[LOGIN_ADMIN]['last_user_id'] + 1
    })

    # push new login profile
    new_profile: dict = {
        "user_id": login_db[LOGIN_ADMIN]['last_user_id'] + 1,
        "username": username,
        "password": password
    }
    db.reference('contacts_mgmt').child('login_db').push(new_profile)

    print(f"Created a new user profile for '{username}'.\n")
    return


def change_login(user: dict) -> None:
    """
    update user profile to change username and/or password

    RULES:
    - username must be less than 24 characters.
    - password must be between 8-12 characters.
    - password must have at least one special character: !@#$%^&*()-_+="
    - password must have at least one number.
    - password must have at least one uppercase.

    :param:
    - profile: user profile (logged in)
    :return: None
    """
    # not allowed to change admin
    if user['username'] == 'admin':
        print("You cannot change the admin account.\n")
        return

    # change username and/or password
    print("Update username and password.")
    print("RULES:")
    print("    - username must be less than 24 characters.")
    print("    - password must be between 8-12 characters.")
    print("    - password must have at least one special character: "
          "!@#$%^&*()-_+=")
    print("    - password must have at least one number.")
    print("    - password must have at least one uppercase.")

    # validate new username
    username: str = input("Username: ")
    if not val_username(username):
        return

    # validate new password
    password: str = input("Password: ")
    if not val_password(password):
        return

    # confirm user action
    while True:
        try:
            print("Are you sure you want to change your profile?")
            is_confirm = input("Please enter 1 for YES or 2 for NO: ")
            is_confirm = int(is_confirm)
        except ValueError as val:
            print(f"{val}. Please enter an integer [1 or 2].")
            continue
        except EOFError:
            raise EOFError("[Exit Contact Management App]")
        else:
            if is_confirm == 1:
                break
            elif is_confirm == 2:
                print("No changes made to your user profile.\n")
                return
            else:
                print("Please enter an integer [1 or 2].")
                continue

    # convert collections object to dict
    login_db: dict = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('login_db').get()
        )
    )

    # update the current user
    for key, val in login_db.items():
        if val["user_id"] == user["user_id"]:
            db.reference('contacts_mgmt').child('login_db').child(key).update({
                'username': username,
                'password': password
            })

    print("Your user profile is updated.\n")
    return


def delete_login(user: dict) -> bool:
    """
    delete the current user profile

    :param: user profile (logged in)
    :return: True/False
    """
    # not allowed to delete admin
    if user['username'] == 'admin':
        print("You cannot delete the admin account.\n")
        return False

    # confirm user action
    while True:
        try:
            print("Are you sure you want to delete your profile?\n"
                  "You will LOSE ALL CONTACTS "
                  "associated with this account as well.")
            is_confirm = input("Please enter 1 for YES or 2 for NO: ")
            is_confirm = int(is_confirm)
        except ValueError as val:
            print(f"{val}. Please enter an integer [1 or 2].")
            continue
        except EOFError:
            raise EOFError("[Exit Contact Management App]")
        else:
            if is_confirm == 1:
                break
            elif is_confirm == 2:
                print("Great choice - stay with us!\n")
                return False
            else:
                print("Please enter an integer [1 or 2].")
                continue

    # convert collections object to dict
    login_db: dict = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('login_db').get()
        )
    )

    # remove the current user
    for key, val in login_db.items():
        if val['user_id'] == user['user_id']:
            db.reference('contacts_mgmt').child('login_db').child(key).delete()

    print("Your user profile is deleted.\n")
    return True


def val_username(username: str) -> bool:
    """
    validate whether username is unique and less than 24 characters.

    :param: username from user input
    :return: True or False
    """
    # convert collections object to dict
    login_db = json.loads(
        json.dumps(
            db.reference('contacts_mgmt').child('login_db').get()
        )
    )

    # username validation (unique and length)
    if len(username) > 24:
        return False

    # check whether `username` already exists
    for profile in login_db.values():
        if profile["username"] == username:
            print(f"'{username}' already exists. "
                  f"Please use a different username.\n")
            return False

    return True


def val_password(password: str) -> bool:
    """
    validate whether password meets the following criteria:
    - password must be between 8-12 characters.
    - password must have at least one special character: !@#$%^&*()-_+="
    - password must have at least one number.
    - password must have at least one uppercase.

    :param: password from user input
    :return: True or False
    """
    specials = "!@#$%^&*()-_+="
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # password validation (4 rules)
    is_length = True if (8 <= len(password) <= 12) else False
    has_symbol = [True for special in specials if special in password]
    has_num = [True for num in nums if num in password]
    has_upper = [True for char in password if char.isupper()]

    if is_length and has_symbol and has_num and has_upper:
        return True

    print("Invalid password. Please follow the rules for password.\n")
    return False


if __name__ == "__main__":
    print("login module")
