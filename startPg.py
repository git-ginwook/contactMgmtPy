import loginPg


# filepath to login database
login_db: str = './login_db.json'


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
            option = input("Please choose a login option [0-4]:\n"
                           "    [0] exit the program\n"
                           "    [1] login with username and password\n"
                           "    [2] create login profile\n"
                           "    [3] change username and password\n"
                           "    [4] delete login profile\n")
            option = int(option)
        except ValueError:
            print("Please enter an integer.")
            continue
        except EOFError:
            raise EOFError("Exit Contact Management App")
        else:
            print(f'You entered option: [{option}]')
            if option == 0:
                break
            if option == 1:
                loginPg.access_login(login_db)
            elif option == 2:
                loginPg.create_login(login_db)
            elif option == 3:
                loginPg.change_login()
            elif option == 4:
                loginPg.delete_login()
            else:
                print("please enter a valid integer between 0 and 4.")
            continue

    print("Thanks for using Contact Management App!")


if __name__ == "__main__":
    main()
