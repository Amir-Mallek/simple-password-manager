from cryptomodule import *
from filemodule import *
import getpass
import os


def print_options(title, options):
    print(f"-{title.title()}-")
    index = 1
    for an_option in options:
        print(f"{index}- {an_option}")
        index += 1


def authenticate(test, expected_result):
    while True:
        typed_password = getpass.getpass('Type your master password: ')
        try:
            testee = decrypt_string(typed_password, test)
            if testee == expected_result:
                log('Correct master password')
                return typed_password
            print('Wrong password! Try again')
        except Exception as e:
            print('Wrong password! Try again')


def change_master_password():
    while True:
        old_password = getpass.getpass('Type your old master password(type n to return): ')
        if old_password.upper() == 'N':
            return masterPassword, encryptedData
        if masterPassword == old_password:
            while True:
                new_password = getpass.getpass('Type your new master password(type n to return): ')
                if new_password.upper() == 'N':
                    return masterPassword, encryptedData
                else:
                    confirm_password = getpass.getpass('Confirm password: ')
                    if confirm_password == new_password:
                        log('Updated password')
                        log(f"Making encrypted backup in '{os.getcwd()}'")
                        make_backup(encryptedData)
                        log('Encrypting data')
                        new_encrypted_data = encrypt_data(new_password, decryptedData)
                        log('Writing new encrypted data')
                        write_data(filePath, new_encrypted_data)
                        return new_password, new_encrypted_data
                    else:
                        print('Wrong password! Try again')
        else:
            print('Wrong password! Try again')


def modify_password(key):
    key = key.upper()
    while True:
        response = input(f"Do you want a generated password for '{key}' (y/N or type q to return):").upper()
        if response == 'Q':
            return
        if response == 'Y':
            log('Generating password')
            new_password = generate_strong_password()
        else:
            new_password = getpass.getpass(f"Type a password for '{key}'(type n return): ")
            if new_password.upper() == 'N':
                return
            else:
                confirm_password = getpass.getpass('Confirm password: ')
                if confirm_password != new_password:
                    print('Wrong password! Try again')
                    continue
        log(f"Making encryted backup in '{os.getcwd()}'")
        make_backup(encryptedData)
        decryptedData[key] = new_password
        encryptedData[key] = encrypt_string(masterPassword, new_password)
        log('Writing new encryted data')
        write_data(filePath, encryptedData)
        return


def get_password():
    while True:
        required = input('Type the required password(type n to return): ')
        if required.upper() == 'N':
            return
        if decryptedData.keys().__contains__(required.upper()):
            print('The password is: ', decryptedData[required.upper()])
            return
        else:
            print(f"No password exists for '{required.upper()}'")


def add_password():
    while True:
        new_key = input('Type the new key(type n return): ').upper()
        if new_key == 'N':
            return
        if decryptedData.keys().__contains__(new_key):
            print(f"You already have a password for '{new_key}'")
        else:
            modify_password(new_key)
            return


def edit_password():
    while True:
        key = input('Type the key for the password to edit(type n to return): ').upper()
        if key == 'N':
            return
        if decryptedData.keys().__contains__(key):
            modify_password(key)
            return
        else:
            print(f"No password exists for '{key}'")


filePath = "C:\\Users\\amirm\\PycharmProjects\\password-manager\\passwords.json"
# toDelete password=123
testKey = 'TEST'
expected = 'haha'

log('Reading encrypted data')
encryptedData = read_data(filePath)
masterPassword = authenticate(encryptedData[testKey], expected)
log('Decrypting data')
decryptedData = decrypt_data(masterPassword, encryptedData)

menuOptions = [
        'Get Password',
        'Add Password',
        'Edit Password',
        'Change Master Password',
        'Exit',
        'See Options'
    ]
print()
print_options('App Options', menuOptions)
while True:
    print()
    option = int(input('Choose an option(1-6). Type 6 to view options: '))
    print()
    match option:
        case 1:
            get_password()
        case 2:
            add_password()
        case 3:
            edit_password()
        case 4:
            masterPassword, encryptedData = change_master_password()
        case 5:
            log('Closing the app')
            break
        case 6:
            print_options('App Options', menuOptions)
        case _:
            print('Invalid option!')
