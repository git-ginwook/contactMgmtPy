# login database format:
# login_db = {<userId>: {<username>, <password>}}

# initialize login DB with admin access
login_db: dict = {0: {"admin", "1234"}}

# count variables
user_id_count: int = 0
user_num_count: int = 0


def access_login():
    username: str = input("Username: ")
    password: str = input("Password: ")

    # check username and password in `login_db`

    # enter contact page


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
