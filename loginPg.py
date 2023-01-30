import json
import contactListPg

# count variables
user_id_count: int = 0
user_num_count: int = 0

# filepath to login database
login_db = './login_db.json'


def access_login() -> None:
    """
    login username and password in `login_db.json`
    """
    is_success = False
    attempt = 0
    max_attempt = 5

    for i in range(attempt, max_attempt):
        try:
            username: str = input("Username: ")
            password: str = input("Password: ")

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


def create_login() -> None:
    """
    create user
    """
    print("create username and password")
    # add a new login profile to `login_db`

    # confirm creation

    # return to `startPg.py`


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
