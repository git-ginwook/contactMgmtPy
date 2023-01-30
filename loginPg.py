import json


# filepath to login database
user_fp: str = './login_db.json'


def access_login() -> bool and dict:
    """
    login username and password in `login_db.json`

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
            raise EOFError("Exit Contact Management App")

        else:
            # read `login_db.json`
            with open(user_fp, "r") as r_login:
                user_db: list = json.load(r_login)

            for profile in user_db:
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
            raise EOFError("Exit Contact Management App")
        else:
            if is_confirm == 1:
                break
            elif is_confirm == 2:
                print("No new user file.\n")
                return
            else:
                print("Please enter an integer [1 or 2].")
                continue

    # read `login_db.json`
    with open(user_fp, "r") as r_login:
        user_db: list = json.load(r_login)

    # append new profile
    new_profile: dict = {
        "user_id": user_db[-1]["user_id"] + 1,
        "username": username,
        "password": password
    }
    user_db.append(new_profile)

    # write new profile to `login_db.json`
    with open(user_fp, "w") as w_login:
        json.dump(user_db, w_login, indent=4)

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
    if len(username) > 24:
        return

    # validate new password
    password: str = input("Password: ")
    is_val = val_password(password)
    if not is_val:
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
            raise EOFError("Exit Contact Management App")
        else:
            if is_confirm == 1:
                break
            elif is_confirm == 2:
                print("No changes made to your user profile.\n")
                return
            else:
                print("Please enter an integer [1 or 2].")
                continue

    # read `login_db.json`
    with open(user_fp, "r") as r_login:
        user_db: list = json.load(r_login)

    # update the current user
    for profile in user_db:
        if profile["user_id"] == user["user_id"]:
            profile["username"] = username
            profile["password"] = password

    # write updated `user_db` to `login_db.json`
    with open(user_fp, "w") as w_login:
        json.dump(user_db, w_login, indent=4)

    print("Your user profile is updated.\n")
    return


def delete_login(user: dict) -> None:
    """
    delete the current user profile

    :param: user profile (logged in)
    :return: None
    """
    # confirm user action
    while True:
        try:
            print("Are you sure you want to delete your profile?")
            is_confirm = input("Please enter 1 for YES or 2 for NO: ")
            is_confirm = int(is_confirm)
        except ValueError as val:
            print(f"{val}. Please enter an integer [1 or 2].")
            continue
        except EOFError:
            raise EOFError("Exit Contact Management App")
        else:
            if is_confirm == 1:
                break
            elif is_confirm == 2:
                print("Great choice - stay with us!\n")
                return
            else:
                print("Please enter an integer [1 or 2].")
                continue

    # read `login_db.json`
    with open(user_fp, "r") as r_login:
        user_db: list = json.load(r_login)

    # remove the current user
    for idx, profile in enumerate(user_db):
        if profile["user_id"] == user["user_id"]:
            user_db.pop(idx)

    # write updated `user_db` to `login_db.json`
    with open(user_fp, "w") as w_login:
        json.dump(user_db, w_login, indent=4)

    print("Your user profile is deleted.\n")
    return


def val_username(username: str) -> bool:
    """
    validate whether username is unique and less than 24 characters.

    :param: username from user input
    :return: True or False
    """
    # read `login_db.json`
    with open(user_fp, "r") as r_login:
        user_db: list = json.load(r_login)

    # username validation (unique and length)
    if len(username) > 24:
        return False

    for profile in user_db:
        if profile["username"] == username:
            print(f"'{username}' already exists. "
                  f"Please use a different username.")
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

    print("Invalid password. Please follow the rules for password.")
    return False


if __name__ == "__main__":
    print("login module")
