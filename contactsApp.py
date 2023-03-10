import firebase_admin
from firebase_admin import credentials
import login
import contacts


def main() -> None:
    """
    start page with login options for user to select from
    :return: None
    """
    # start Contact Management App
    print("\n[Welcome to Contact Management App]")
    print("Manage your professional network efficiently in one place.")
    print("You can view, create, update, and delete your contact.")
    print("With our login feature, your contact list is private.\n")

    # Choose login option
    while True:
        try:
            option = input(
                "Please choose a login option [0 ~ 5]:\n"
                "    [0] exit the program\n"
                "    [1] login with username and password (account needed)\n"
                "    [2] create login profile\n"
                "    [3] change username and password (login required)\n"
                "    [4] delete login profile (login required)\n"
                "    [5] contact developer for any questions or feedback\n")
            option = int(option)
        except ValueError as val:
            print(f"{val}. Please enter an integer [0 ~ 5].")
            continue
        except EOFError:
            raise EOFError("[Exit Contact Management App]")
        else:
            print(f'Your login option: [{option}]')
            if option == 0:
                break
            if option == 1:
                is_login, user = login.access_login()

                # access contacts for `user_id`
                if is_login:
                    if contacts.view_all(user["user_id"]):
                        contacts.view_all(user["user_id"])

            elif option == 2:
                login.create_login()
            elif option == 3:
                is_login, user = login.access_login()
                if is_login:
                    login.change_login(user)
            elif option == 4:
                is_login, user = login.access_login()
                if is_login:
                    if login.delete_login(user):
                        contacts.delete_all(user["user_id"])
            elif option == 5:
                print("Please send your questions or comments to: "
                      "leeginw@oregonstate.edu\n")
            else:
                print("Please enter an integer [0 ~ 5].")
            continue

    print("Thanks for using Contact Management App!")


if __name__ == "__main__":
    # refer to the credential key (json file)
    CRED = credentials.Certificate(
        "/Users/ginwooklee_air/Library/CloudStorage/Box-Box/6_Winter23/CS361/contactMgmtPy"
        "/microservices/contactsmgmt-8647c-firebase-adminsdk-8c4vb-12ede2dd14.json"
    )

    # initialize `firebase_admin`
    firebase_admin.initialize_app(CRED, {
        'databaseURL': "https://contactsmgmt-8647c-default-rtdb.firebaseio.com/"
    })

    main()
