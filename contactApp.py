import json
import loginPg
import contactListPg


def main() -> None:
    """
    start page with login options for user to select from

    :return: None
    """
    # start Contact Management App
    print("[Contact Management App]")

    # Choose login option
    while True:
        try:
            option = input("Please choose a login option [0 ~ 4]:\n"
                           "    [0] exit the program\n"
                           "    [1] login with username and password\n"
                           "    [2] create login profile\n"
                           "    [3] change username and password\n"
                           "    [4] delete login profile\n")
            option = int(option)
            is_login: bool = False
        except ValueError as val:
            print(f"{val}. Please enter an integer [0 ~ 4].")
            continue
        except EOFError:
            raise EOFError("Exit Contact Management App")
        else:
            print(f'You entered option: [{option}]')
            if option == 0:
                break
            if option == 1:
                is_login, user = loginPg.access_login()
                if is_login:
                    # move to contactListPg.py
                    contactListPg.view_contact(user["user_id"])
            elif option == 2:
                loginPg.create_login()
            elif option == 3:
                is_login, user = loginPg.access_login()
                if is_login:
                    loginPg.change_login(user)
            elif option == 4:
                is_login, user = loginPg.access_login()
                if is_login:
                    loginPg.delete_login(user)
            else:
                print("Please enter an integer [0 ~ 4].")
            continue

    print("Thanks for using Contact Management App!")


if __name__ == "__main__":
    main()
