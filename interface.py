import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog, QLabel, QLineEdit, QHBoxLayout, QStackedWidget

from cryptomodule import *
from filemodule import *
import os


class PasswordManagerGUI(QMainWindow):
    central_widget = QStackedWidget()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Password Manager')
        self.setGeometry(200, 200, 500, 200)
        self.setCentralWidget(PasswordManagerGUI.central_widget)

    @staticmethod
    def show_menu():
        menu_widget = MenuWidget()
        PasswordManagerGUI.central_widget.addWidget(menu_widget)
        PasswordManagerGUI.central_widget.setCurrentWidget(menu_widget)

    def init_get_password_view(self):
        self.get_password_widget = QWidget()
        self.get_password_layout = QVBoxLayout()

        self.key_input = QLineEdit(self.get_password_widget)
        self.key_input.setPlaceholderText('Enter key for password')
        self.get_password_layout.addWidget(self.key_input)

        self.password_display = QLineEdit(self.get_password_widget)
        self.password_display.setEchoMode(QLineEdit.Password)
        self.password_display.setReadOnly(True)
        self.get_password_layout.addWidget(self.password_display)

        button_layout = QHBoxLayout()

        self.show_password_btn = QPushButton('Show', self.get_password_widget)
        self.show_password_btn.setCheckable(True)
        self.show_password_btn.toggled.connect(self.toggle_password_visibility)
        button_layout.addWidget(self.show_password_btn)

        self.copy_password_btn = QPushButton('Copy', self.get_password_widget)
        self.copy_password_btn.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_password_btn)

        self.return_btn = QPushButton('Return', self.get_password_widget)
        self.return_btn.clicked.connect(self.show_menu_view)
        button_layout.addWidget(self.return_btn)

        self.get_password_layout.addLayout(button_layout)
        self.get_password_widget.setLayout(self.get_password_layout)

    def show_get_password_view(self):
        self.setCentralWidget(self.get_password_widget)

    def show_menu_view(self):
        self.stack.setCurrentWidget(self.menu_widget)

    def authenticate(self, test, expected_result):
        label = 'Type your master password:'
        while True:
            typed_password, ok = QInputDialog.getText(
                self,
                'Authenticate',
                label,
                QLineEdit.Password
            )
            if ok:
                try:
                    testee = decrypt_string(typed_password, test)
                    if testee == expected_result:
                        log('Correct master password')
                        return typed_password
                except Exception:
                    pass
                label = 'Wrong password! Try again'

    def get_password(self):
        required, ok = QInputDialog.getText(self, 'Get Password', 'Type the required password:')
        if ok and required:
            required = required.upper()
            if required in decryptedData:
                self.password_display = QLineEdit(self)
                self.password_display.setText('*' * len(decryptedData[required]))
                self.password_display.setEchoMode(QLineEdit.Password)
                self.password_display.setReadOnly(True)

                # Layout for buttons
                button_layout = QHBoxLayout()

                # Show/Hide button
                self.show_password_btn = QPushButton('Show', self)
                self.show_password_btn.setCheckable(True)
                self.show_password_btn.toggled.connect(self.toggle_password_visibility)
                button_layout.addWidget(self.show_password_btn)

                # Copy button
                self.copy_password_btn = QPushButton('Copy', self)
                self.copy_password_btn.clicked.connect(lambda: self.copy_to_clipboard(decryptedData[required]))
                button_layout.addWidget(self.copy_password_btn)

                # Add the password display and buttons to the layout
                self.main_layout.addWidget(self.password_display)
                self.main_layout.addLayout(button_layout)
            else:
                self.label.setText(f"No password exists for '{required}'")

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_display.setEchoMode(QLineEdit.Normal)
            self.show_password_btn.setText('Hide')
        else:
            self.password_display.setEchoMode(QLineEdit.Password)
            self.show_password_btn.setText('Show')

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.label.setText('Password copied to clipboard')

    def add_password(self):
        # Implement similarly to the get_password method
        pass

    def edit_password(self):
        # Implement similarly to the get_password method
        pass

    def change_master_password(self):
        # Implement the change_master_password logic with appropriate dialogs
        pass


class MenuWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.label = QLabel('Choose an option:', self)
        self.layout.addWidget(self.label)

        self.get_password_btn = QPushButton('Get Password', self)
        self.get_password_btn.clicked.connect(self.hello)
        self.layout.addWidget(self.get_password_btn)

        self.add_password_btn = QPushButton('Add Password', self)
        self.add_password_btn.clicked.connect(self.hello)
        self.layout.addWidget(self.add_password_btn)

        self.edit_password_btn = QPushButton('Edit Password', self)
        self.edit_password_btn.clicked.connect(self.hello)
        self.layout.addWidget(self.edit_password_btn)

        self.change_master_password_btn = QPushButton('Change Master Password', self)
        self.change_master_password_btn.clicked.connect(self.hello)
        self.layout.addWidget(self.change_master_password_btn)

        self.exit_btn = QPushButton('Exit', self)
        self.exit_btn.clicked.connect(self.hello)
        self.layout.addWidget(self.exit_btn)

        self.setLayout(self.layout)

    def hello(self):
        log('hello')


class AuthWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.layout = QVBoxLayout()

        self.label = QLabel('Enter Master Password:', self)
        self.layout.addWidget(self.label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.authenticate)
        self.layout.addWidget(self.login_button)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.cancel)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def authenticate(self):
        password = self.password_input.text()


    def cancel(self):
        self.main_window.close()  # Exit the application or handle as needed


if __name__ == '__main__':
    app = QApplication(sys.argv)

    filePath = "C:\\Users\\amirm\\PycharmProjects\\password-manager\\passwords.json"
    testKey = 'TEST'
    expected = 'haha'

    log('Reading encrypted data')
    encryptedData = read_data(filePath)

    # Create an instance of the application window
    window = PasswordManagerGUI()

    # Authenticate user
    masterPassword = window.authenticate(encryptedData[testKey], expected)
    log('Decrypting data')
    decryptedData = decrypt_data(masterPassword, encryptedData)

    # Show the window
    window.show()

    sys.exit(app.exec_())
