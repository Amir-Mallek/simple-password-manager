from cryptomodule import *
from filemodule import *
import os


class Manager:
    filePath = "C:\\Users\\amirm\\PycharmProjects\\password-manager\\passwords.json"
    # toDelete password=123
    testKey = 'TEST'
    expected = 'haha'

    def __init__(self):
        log('Reading encrypted data')
        self.encryptedData = read_data(Manager.filePath)
        self.decryptedData = None
        self.isAuth = False
        self.masterPassword = None

    def authenticate(self, password):
        try:
            log('Authenticating')
            test = self.encryptedData[Manager.testKey]
            testee = decrypt_string(password, test)
            if testee == Manager.expected:
                log('Successfull Authentication')
                self.isAuth = True
                self.masterPassword = password
                return True
            log('Failed Authentication')
        except Exception as e:
            log('Failed Authentication')
            print(e)
            return False

    def check_password(self, password):
        log('Checking password')
        if self.isAuth:
            return self.masterPassword == password
        return False

    def set_decrypt_data(self):
        if self.isAuth:
            log('Decrypting data')
            self.decryptedData = decrypt_data(self.masterPassword, self.encryptedData)

    def get_decrypted_data(self):
        if self.decryptedData is not None:
            return self.decryptedData
        self.set_decrypt_data()
        return self.decryptedData

    def get_password(self, key):
        key = key.upper()
        log(f"Getting password for '{key}'")
        if self.isAuth and self.get_decrypted_data().keys().__contains__(key):
            return self.get_decrypted_data()[key]
        return None

    def add_password(self, key, password):
        log(f"Adding password for '{key}'")
        if self.isAuth and not self.decryptedData.keys().__contains__(key):
            log(f"Making encryted backup in '{os.getcwd()}'")
            make_backup(self.encryptedData)
            self.decryptedData[key] = password
            self.encryptedData[key] = encrypt_string(self.masterPassword, password)
            log('Writing new encryted data')
            write_data(Manager.filePath, self.encryptedData)