import loginPg


def main() -> None:
    # start Contact Management App
    print("[Contact Management App]")

    # Choose login option
    while True:
        try:
            option = input("Please choose a login option [1-4]:\n"
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
            print(f'You entered: {option}')
            if option == 1:
                loginPg.access_login()
            elif option == 2:
                loginPg.create_login()
            elif option == 3:
                loginPg.change_login()
            elif option == 4:
                loginPg.delete_login()
            else:
                print("please enter a valid integer between 1 and 4.")
                continue
            break


if __name__ == "__main__":
    main()
