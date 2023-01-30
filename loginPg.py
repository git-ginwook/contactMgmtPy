import json
import contactListPg


def access_login(login_db: str) -> None:
    """
    login username and password in `login_db.json`
    """
    is_success: bool = False
    attempt: int = 1
    max_attempt: int = 5

    print("login with your username and password")
    for i in range(attempt, max_attempt+1):
        try:
            # get user inputs
            username: str = input("Username: ")
            password: str = input("Password: ")

            # read login_db.json
            with open(login_db, "r") as f_login:
                db = json.load(f_login)

        except EOFError:
            raise EOFError("Exit Contact Management App")

        else:
            for profile in db:
                if profile["username"] == username and \
                        profile["password"] == password:
                    is_success = True
                    print("login was successful!")
                    # move to contactListPg.py
                    contactListPg.view_contact(profile["user_id"])

            if (not is_success) and (attempt < max_attempt):
                print("username and password don't match - please try again. "
                      f"[{attempt}/{max_attempt}]")
                attempt += 1
                continue
            elif (not is_success) and (attempt == max_attempt):
                print("Too many wrong attempts. "
                      f"[{attempt}/{max_attempt}]")
                attempt = 0
            break
    return


def create_login(login_db: str) -> None:
    """
    create a user profile with username and password

    RULES:
    - username must be UNIQUE.
    - password must be between 8-12 characters.
    - password must have at least one special character: !@#$%^&*()-_+="
    - password must have at least one number.
    - password must have at least one uppercase.
    """
    specials = "!@#$%^&*()-_+="
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # flags
    is_unique = True
    is_length = False
    has_symbol = False
    has_num = False
    has_upper = False
    is_val = False

    print("create username and password.")
    print("RULES:")
    print("    - username must be UNIQUE.")
    print("    - password must be between 8-12 characters.")
    print("    - password must have at least one special character: "
          "!@#$%^&*()-_+=")
    print("    - password must have at least one number.")
    print("    - password must have at least one uppercase.")

    # read `login_db.json`
    with open(login_db, "r") as f_login:
        db = json.load(f_login)

    # get username
    username: str = input("Username: ")

    # username validation (UNIQUE)
    for profile in db:
        if profile["username"] == username:
            print(f"'{username}' already exists. "
                  f"Please use a different username.")
            is_unique = False
            break

    if not is_unique:
        return

    # get password
    password: str = input("Password: ")

    # password validation (4 rules)
    is_length = True if (8 < len(password) < 12) else False
    has_symbol = [True for special in specials if special in password]
    has_num = [True for num in nums if num in password]
    has_upper = [True for char in password if char.isupper()]

    if is_length and has_symbol and has_num and has_upper:
        is_val = True

    if not is_val:
        print("Invalid password. Please follow the rules for password.")
        return

    # append new profile
    new_profile: dict = {
        "user_id": db[-1]["user_id"] + 1,
        "username": username,
        "password": password
    }
    db.append(new_profile)

    # write new profile to `login_db.json`
    with open(login_db, "w") as f_login:
        json.dump(db, f_login, indent=4)

    print(f"Created a new user profile for '{username}'.")
    return


def change_login():
    # change username and/or password

    # confirm change

    # return to `startPg.py`
    pass


def delete_login():
    # delete login profile

    # confirm username and password

    # confirm deletion

    # return to `startPg.py`
    pass


if __name__ == "__main__":
    print("login module")
