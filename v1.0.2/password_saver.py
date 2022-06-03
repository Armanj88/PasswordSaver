import pickle
import os
import time
import ctypes

password_entered = False

os.system("cls")


# check is user with administrator rights or not
def is_admin():
    is_admin = False
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin


if is_admin():
    # make sure files and directorys exists
    os.system("cd %CD%")

    if not os.path.exists("data"):
        os.mkdir("data")

    try:
        with open("data/login_password.data", "rb") as f:
            pickle.load(f)
        with open("data/passwords.data", "rb") as f:
            pickle.load(f)
    except:
        with open("data/login_password.data", "wb") as f:
            pickle.dump("admin", f)
        with open("data/passwords.data", "wb") as f:
            pickle.dump([], f)


    def pause():
        os.system("pause")

    # login to application


    def enter_password():
        password = input(
            "Enter password to login and confirm you have permission: ")
        with open("data/login_password.data", "rb") as f:
            if password == pickle.load(f):
                print("Done!")
                password_entered = True
            else:
                print("Wrong!")
                time.sleep(2)
                os._exit(0)
        return password_entered


    password_entered = enter_password()
    if password_entered != True:
        password_entered = enter_password()
        enter_password()


    def add_password():
        # add new password to passwords list
        with open("data/passwords.data", "rb") as f:
            passwords_list = pickle.load(f)
        with open("data/passwords.data", "wb") as f:
            # get password
            password_to_save = input(
                "Enter your password that you like to save: ")
            password_name_to_save = input(
                "Enter password name to find it easily: ")

            # encrypt password
            password_to_save_ascii = ""
            password_to_save_ascii_list = []
            for i in password_to_save:
                password_to_save_ascii += str(ord(i))
                password_to_save_ascii_list.append(str(ord(i)))

            password_name_to_save_ascii = ""
            password_name_to_save_ascii_list = []
            for i in password_name_to_save:
                password_name_to_save_ascii += str(ord(i))
                password_name_to_save_ascii_list.append(str(ord(i)))

            # append to full list
            password_full = {"name": password_name_to_save,
                            "password": password_to_save_ascii,
                            "list_password_ascii": password_to_save_ascii_list,
                            "list_password_name_ascii": password_name_to_save_ascii_list}
            passwords_list.append(password_full)
            pickle.dump(passwords_list, f)


    def remove_password():
        # remove password from passwords list
        print("Note: You can find passwords by name in \"show passwords\" command")
        password_name_to_remove = input("Enter password name to remove: ")
        with open("data/passwords.data", "rb") as f:
            passwords_list = pickle.load(f)
            if password_name_to_remove == "*":
                passwords_list.clear()
            else:
                for i in passwords_list:
                    if i[list(i.keys())[0]] == password_name_to_remove:
                        passwords_list.remove(i)
                        break
        with open("data/passwords.data", "wb") as f:
            pickle.dump(passwords_list, f)


    def show_passwords():
        # show all passwords list
        with open("data/passwords.data", "rb") as f:
            passwords_list = pickle.load(f)
            for i in passwords_list:
                # set password variables
                password_name = i["name"]
                password_password = i["password"]
                password_ascii_list = i["list_password_ascii"]
                password_name_ascii_list = i["list_password_name_ascii"]

                # decrypt password variables
                password_password_encrypted = ""
                for i in password_ascii_list:
                    password_password_encrypted += chr(int(i))

                password_name_encrypted = ""
                for i in password_name_ascii_list:
                    password_name_encrypted += chr(int(i))

                # print password name and orginal password
                print("Name: {}\nPassword: {}\n".format(
                    password_name_encrypted, password_password_encrypted))
        pause()


    while True:
        if password_entered:
            print("""
            [1] Add new password
            [2] Delete a password
            [3] Show all passwords
            [4] Exit   
            """)
            choice = input("[?]: ")
            if choice == "1":
                add_password()
            elif choice == "2":
                remove_password()
            elif choice == "3":
                show_passwords()
            else:
                os._exit(0)
        os.system("cls")

else:
    print("You don't have permission to use this application!\nPlease run it again with administrator rights.")
    time.sleep(5)
    os._exit(0)