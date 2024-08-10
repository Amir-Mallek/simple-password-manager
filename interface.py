import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QPushButton, QVBoxLayout, QWidget, QSizePolicy, QLabel, QLineEdit, QHBoxLayout, QStackedWidget
from PyQt5.QtGui import QIcon
from manager import *


class PasswordManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Password Manager')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(400, 400, 500, 50)

        self.global_style_sheet = """
            QMainWindow {
                background-color: white;
            }
            QPushButton {
                background-color: #4c9faf;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                font-weight: bold;
                margin: 4px 2px;
                border-radius: 5px;
                font-family: 'Arial';
            }
            QLabel {
                height: fit-content;
                font-size: 16px;
                color: #333;
                font-family: 'Arial';
                font-weight: bold;
            }
            QLabel.error {
                color: red;
                font-weight: bold;
            }
            QLabel.success {
                color: green;
                font-weight: bold;
            }
            QLineEdit {
                color: #4c9faf; 
                font-size: 16px; 
                font-weight: bold;
                background-color: #f9f9f9;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-family: 'Arial';
            }
            QLineEdit.password {
                color: black;
                font-weight: normal;
            }
        """
        self.setStyleSheet(self.global_style_sheet)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.show_auth()

    def show_menu(self):
        menu_widget = MenuWidget(self)
        self.central_widget.addWidget(menu_widget)
        self.central_widget.setCurrentWidget(menu_widget)

    def show_auth(self):
        auth_widget = AuthWidget(self)
        self.central_widget.addWidget(auth_widget)
        self.central_widget.setCurrentWidget(auth_widget)

    def show_get_password(self):
        get_password_widget = GetPasswordWidget(self)
        self.central_widget.addWidget(get_password_widget)
        self.central_widget.setCurrentWidget(get_password_widget)

    def show_add_password(self):
        add_password_widget = AddPasswordWidget(self)
        self.central_widget.addWidget(add_password_widget)
        self.central_widget.setCurrentWidget(add_password_widget)

    def show_edit_password(self):
        edit_password_widget = EditPasswordWidget(self)
        self.central_widget.addWidget(edit_password_widget)
        self.central_widget.setCurrentWidget(edit_password_widget)

    def show_change_master_password(self):
        change_master_password_widget = ChangeMasterPasswordWidget(self)
        self.central_widget.addWidget(change_master_password_widget)
        self.central_widget.setCurrentWidget(change_master_password_widget)


class MenuWidget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.layout = QVBoxLayout()

        self.label = QLabel('Application Menu', self)
        self.label.setStyleSheet('font-size: 24px; font-weight: bold;')
        self.layout.addWidget(self.label)

        self.get_password_btn = QPushButton('Get Password', self)
        self.get_password_btn.clicked.connect(main_window.show_get_password)
        self.layout.addWidget(self.get_password_btn)

        self.add_password_btn = QPushButton('Add Password', self)
        self.add_password_btn.clicked.connect(main_window.show_add_password)
        self.layout.addWidget(self.add_password_btn)

        self.edit_password_btn = QPushButton('Edit Password', self)
        self.edit_password_btn.clicked.connect(main_window.show_edit_password)
        self.layout.addWidget(self.edit_password_btn)

        self.change_master_password_btn = QPushButton('Change Master Password', self)
        self.change_master_password_btn.clicked.connect(main_window.show_change_master_password)
        self.layout.addWidget(self.change_master_password_btn)

        self.exit_btn = QPushButton('Exit', self)
        self.exit_btn.clicked.connect(main_window.close)
        self.exit_btn.setStyleSheet('background-color: red')
        self.layout.addWidget(self.exit_btn)

        self.setLayout(self.layout)


class AuthWidget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window

        self.layout = QVBoxLayout()

        self.label = QLabel('Enter Master Password:', self)
        self.layout.addWidget(self.label)

        self.incorrect_label = QLabel('Incorrect Password !', self)
        self.incorrect_label.setProperty('class', 'error')
        self.incorrect_label.hide()
        self.layout.addWidget(self.incorrect_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setProperty('class', 'password')
        self.layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.authenticate)
        self.login_button.setStyleSheet('background-color: green')
        button_layout.addWidget(self.login_button)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(main_window.close)
        self.cancel_button.setStyleSheet('background-color: red')
        button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def authenticate(self):
        password = self.password_input.text()
        if manager.authenticate(password):
            self.close()
            self.main_window.show_menu()
        else:
            self.incorrect_label.show()


class GetPasswordWidget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.layout = QVBoxLayout()

        self.label = QLabel('Enter Key:', self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.label)

        self.info_label = QLabel('', self)
        self.info_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.info_label.hide()
        self.layout.addWidget(self.info_label)

        self.key_input = QLineEdit(self)
        self.layout.addWidget(self.key_input)

        button_layout = QHBoxLayout()

        self.get_password_btn = QPushButton('Get Password', self)
        self.get_password_btn.clicked.connect(self.get_password)
        self.get_password_btn.setStyleSheet('background-color: green')
        button_layout.addWidget(self.get_password_btn)

        self.return_btn = QPushButton('Return', self)
        self.return_btn.clicked.connect(main_window.show_menu)
        self.return_btn.setStyleSheet('background-color: red')
        button_layout.addWidget(self.return_btn)

        self.layout.addLayout(button_layout)

        self.password_display = QLineEdit(self)
        self.password_display.setEchoMode(QLineEdit.Password)
        self.password_display.setReadOnly(True)
        self.password_display.setProperty('class', 'password')
        self.password_display.hide()
        self.layout.addWidget(self.password_display)

        usage_button_layout = QHBoxLayout()

        self.show_password_btn = QPushButton('Show', self)
        self.show_password_btn.setCheckable(True)
        self.show_password_btn.toggled.connect(self.toggle_password_visibility)
        self.show_password_btn.hide()
        usage_button_layout.addWidget(self.show_password_btn)

        self.copy_password_btn = QPushButton('Copy', self)
        self.copy_password_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_password_btn.hide()
        usage_button_layout.addWidget(self.copy_password_btn)

        self.layout.addLayout(usage_button_layout)

        self.setLayout(self.layout)

    def get_password(self):
        key = self.key_input.text()
        password = manager.get_password(key)
        if password is not None:
            self.info_label.setText('Operation successful !')
            self.info_label.setProperty('class', 'success')
            self.password_display.setText(password)
            self.password_display.show()
            self.show_password_btn.show()
            self.copy_password_btn.show()
        else:
            self.info_label.setText('Key not found !')
            self.info_label.setProperty('class', 'error')
            self.password_display.hide()
            self.show_password_btn.hide()
            self.copy_password_btn.hide()
        self.info_label.setStyleSheet(self.info_label.styleSheet())
        self.info_label.show()

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_display.setEchoMode(QLineEdit.Normal)
            self.show_password_btn.setText('Hide')
        else:
            self.password_display.setEchoMode(QLineEdit.Password)
            self.show_password_btn.setText('Show')

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_display.text())


class EditPasswordWidget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window

        self.layout = QVBoxLayout()

        self.label = QLabel('Enter Key:', self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.label)

        self.key_input = QLineEdit(self)
        self.layout.addWidget(self.key_input)

        password_layout = QHBoxLayout()

        self.label = QLabel('Enter New Password:', self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        password_layout.addWidget(self.label)

        self.generate_password_btn = QPushButton('Generate Password', self)
        self.generate_password_btn.clicked.connect(self.generate_password)
        password_layout.addWidget(self.generate_password_btn)

        self.layout.addLayout(password_layout)

        self.password_input = QLineEdit(self)
        self.password_input.setProperty('class', 'password')
        self.layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()

        self.info_label = QLabel('', self)
        self.info_label.hide()
        self.info_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.info_label)

        self.edit_password_btn = QPushButton('Edit Password', self)
        self.edit_password_btn.clicked.connect(self.edit_password)
        self.edit_password_btn.setStyleSheet('background-color: green')
        button_layout.addWidget(self.edit_password_btn)

        self.return_btn = QPushButton('Return', self)
        self.return_btn.clicked.connect(main_window.show_menu)
        self.return_btn.setStyleSheet('background-color: red')
        button_layout.addWidget(self.return_btn)

        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def edit_password(self):
        key = self.key_input.text()
        password = self.password_input.text()
        if manager.update_password(key, password):
            self.info_label.setText('Password edited successfully !')
            self.info_label.setProperty('class', 'success')
        else:
            self.info_label.setText('Key not found !')
            self.info_label.setProperty('class', 'error')
        self.info_label.show()
        self.info_label.setStyleSheet(self.info_label.styleSheet())

    def generate_password(self):
        generated_password = manager.generate_password()
        self.password_input.setText(generated_password)


class AddPasswordWidget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window

        self.layout = QVBoxLayout()

        self.label = QLabel('Enter New Key:', self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.label)

        self.key_input = QLineEdit(self)
        self.layout.addWidget(self.key_input)

        password_layout = QHBoxLayout()

        self.label = QLabel('Enter Password:', self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        password_layout.addWidget(self.label)

        self.generate_password_btn = QPushButton('Generate Password', self)
        self.generate_password_btn.clicked.connect(self.generate_password)
        password_layout.addWidget(self.generate_password_btn)

        self.layout.addLayout(password_layout)

        self.password_input = QLineEdit(self)
        self.password_input.setProperty('class', 'password')
        self.layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()

        self.info_label = QLabel('', self)
        self.info_label.hide()
        self.info_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.info_label)

        self.add_password_btn = QPushButton('Add Password', self)
        self.add_password_btn.clicked.connect(self.add_password)
        self.add_password_btn.setStyleSheet('background-color: green')
        button_layout.addWidget(self.add_password_btn)

        self.return_btn = QPushButton('Return', self)
        self.return_btn.clicked.connect(main_window.show_menu)
        self.return_btn.setStyleSheet('background-color: red')
        button_layout.addWidget(self.return_btn)

        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def add_password(self):
        key = self.key_input.text()
        password = self.password_input.text()
        if manager.add_password(key, password):
            self.info_label.setText('Password added successfully !')
            self.info_label.setProperty('class', 'success')
        else:
            self.info_label.setText('Key already exists !')
            self.info_label.setProperty('class', 'error')
        self.info_label.show()
        self.info_label.setStyleSheet(self.info_label.styleSheet())

    def generate_password(self):
        generated_password = manager.generate_password()
        self.password_input.setText(generated_password)


class ChangeMasterPasswordWidget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window

        self.layout = QVBoxLayout()

        self.old_label = QLabel('Enter Old Master Password:', self)
        self.old_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.old_label)

        self.old_password_input = QLineEdit(self)
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.old_password_input.setProperty('class', 'password')
        self.layout.addWidget(self.old_password_input)

        self.label = QLabel('Enter New Master Password:', self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setProperty('class', 'password')
        self.layout.addWidget(self.password_input)

        self.confirm_label = QLabel('Confirm New Master Password:', self)
        self.confirm_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.confirm_label)

        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setProperty('class', 'password')
        self.layout.addWidget(self.confirm_password_input)

        self.view_password_btn = QPushButton('View Password', self)
        self.view_password_btn.setCheckable(True)
        self.view_password_btn.toggled.connect(self.toggle_password_visibility)
        self.layout.addWidget(self.view_password_btn)

        self.info_label = QLabel('', self)
        self.info_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.info_label.hide()
        self.layout.addWidget(self.info_label)

        button_layout = QHBoxLayout()

        self.change_password_btn = QPushButton('Change Password', self)
        self.change_password_btn.clicked.connect(self.change_password)
        self.change_password_btn.setStyleSheet('background-color: green')
        button_layout.addWidget(self.change_password_btn)

        self.return_btn = QPushButton('Return', self)
        self.return_btn.clicked.connect(main_window.show_menu)
        self.return_btn.setStyleSheet('background-color: red')
        button_layout.addWidget(self.return_btn)

        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.confirm_password_input.setEchoMode(QLineEdit.Normal)
            self.view_password_btn.setText('Hide Password')
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.confirm_password_input.setEchoMode(QLineEdit.Password)
            self.view_password_btn.setText('View Password')

    def change_password(self):
        old_password = self.old_password_input.text()
        new_password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        if manager.check_password(old_password):
            if new_password == confirm_password:
                manager.change_master_password(new_password)
                self.info_label.setText('Password changed successfully !')
                self.info_label.setProperty('class', 'success')
            else:
                self.info_label.setText('Passwords do not match !')
                self.info_label.setProperty('class', 'error')
        else:
            self.info_label.setText('Incorrect Old Password !')
            self.info_label.setProperty('class', 'error')
        self.info_label.show()
        self.info_label.setStyleSheet(self.info_label.styleSheet())


if __name__ == '__main__':
    manager = Manager()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    window = PasswordManagerGUI()
    window.show()
    sys.exit(app.exec_())

