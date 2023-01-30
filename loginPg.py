import json
import contactListPg


def access_login(login_db: str) -> None:
    """
    login username and password in `login_db.json`
    """
    is_success: bool = False
    attempt: int = 0
    max_attempt: int = 5

    for i in range(attempt, max_attempt):
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

            if (is_success is False) and (attempt < max_attempt):
                print("username and password don't match - please try again. "
                      f"[{attempt+1}/{max_attempt}]")
                attempt += 1
                continue
            elif (is_success is False) and (attempt == max_attempt):
                print("Too many wrong attempts. "
                      f"[{attempt+1}/{max_attempt}]")
                attempt = 0

            break


def create_login(login_db: str) -> None:
    """
    create UNIQUE username and password

    password validation
    - length: 8-12 characters
    - special character: !@#$%^&*()-_+=
    - one number
    - one upper case
    """
    print("create username and password")
    # get user inputs
    username: str = input("Username: ")
    password: str = input("Password: ")

    # username validation (UNIQUE)

    # password validation (rules)

    # read `login_db.json`
    with open(login_db, "r") as f_login:
        db = json.load(f_login)

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

    # confirm creation

    # return to `startPg.py`
    print(f"create a new user profile for '{username}'.")


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
