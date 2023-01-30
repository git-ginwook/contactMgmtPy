import contactListPg


# login database format:
# login_db = {<username>: [<user_id>, <password>]}

# initialize login DB with admin access
login_db: dict = {"admin": [0, "1234"]}

# count variables
user_id_count: int = 0
user_num_count: int = 0


def access_login() -> None:
    """
    check username and password in `login_db`
    """
    attempt = 1
    max_attempt = 5

    while True:
        try:
            username: str = input("Username: ")
            password: str = input("Password: ")

            login_db[username]
        except KeyError:
            print("username doesn't exist.")
            continue
        except EOFError:
            raise EOFError("Exit Contact Management App")
        else:
            if login_db[username][1] == password:
                print("login successful!")
                # move to contactListPg.py
                contactListPg.view_contact(login_db[username][0])
                break

            else:
                if attempt < max_attempt:
                    print(f"wrong password - please try again. "
                          f"[{attempt}/{max_attempt}]")
                    attempt += 1
                    continue
                else:
                    print(f"Too many wrong attempts. "
                          f"[{attempt}/{max_attempt}]")
                    attempt = 0
                    break


def create_login():
    # add a new login profile to `login_db`

    # confirm creation

    # return to `startPg.py`
    pass


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
