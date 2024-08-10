import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QPushButton, QVBoxLayout, QWidget, QSizePolicy, QLabel, QLineEdit, QHBoxLayout, QStackedWidget
from manager import *


class PasswordManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Password Manager')
        self.setGeometry(400, 400, 500, 50)

        qlineeditsheet = """
            
        """

        self.global_style_sheet = """
            QPushButton {
                background-color: #4c9faf;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                font-weight: bold;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px;
                font-family: 'Arial';
            }
            QLabel {
                height: fit-content;
                font-size: 16px;
                color: #333;
                background-color: #f9f9f9;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-family: 'Arial';
                font-weight: bold;
            }
            QLabel.error {
                color: red;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #f9f9f9;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: x-large;
                font-weight: bold;
                font-family: 'Arial';
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


class MenuWidget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.layout = QVBoxLayout()

        self.label = QLabel('Choose an option:', self)
        self.layout.addWidget(self.label)

        self.get_password_btn = QPushButton('Get Password', self)
        self.get_password_btn.clicked.connect(main_window.show_get_password)
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
        self.exit_btn.setStyleSheet('background-color: red')
        self.layout.addWidget(self.exit_btn)

        self.setLayout(self.layout)

    def hello(self):
        log('hello')


class AuthWidget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window

        self.layout = QVBoxLayout()

        self.label = QLabel('Enter Master Password:', self)
        self.layout.addWidget(self.label)

        self.incorrect_label = QLabel('Incorrect Password', self)
        self.incorrect_label.setObjectName('error')
        self.incorrect_label.hide()
        self.layout.addWidget(self.incorrect_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
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
        self.main_window = main_window

        self.layout = QVBoxLayout()

        self.label = QLabel('Enter Key:', self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.label)

        self.incorrect_label = QLabel('Key does not exist!', self)
        self.incorrect_label.setProperty('class', 'error')
        self.incorrect_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.incorrect_label.hide()
        self.incorrect_label.setProperty('class', 'error')
        self.layout.addWidget(self.incorrect_label)

        self.key_input = QLineEdit(self)
        self.layout.addWidget(self.key_input)

        button_layout = QHBoxLayout()

        self.get_password_btn = QPushButton('Get Password', self)
        self.get_password_btn.clicked.connect(self.get_password)
        self.get_password_btn.setStyleSheet('background-color: green')
        button_layout.addWidget(self.get_password_btn)

        self.return_btn = QPushButton('Return', self)
        self.return_btn.clicked.connect(self.show_menu)
        self.return_btn.setStyleSheet('background-color: red')
        button_layout.addWidget(self.return_btn)

        self.layout.addLayout(button_layout)

        self.password_display = QLineEdit(self)
        self.password_display.setEchoMode(QLineEdit.Password)
        self.password_display.setReadOnly(True)
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
            self.incorrect_label.hide()
            self.password_display.setText(password)
            self.password_display.show()
            self.show_password_btn.show()
            self.copy_password_btn.show()
        else:
            self.password_display.hide()
            self.show_password_btn.hide()
            self.copy_password_btn.hide()
            self.incorrect_label.show()

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

    def show_menu(self):
        self.main_window.show_menu()


if __name__ == '__main__':
    manager = Manager()
    app = QApplication(sys.argv)
    window = PasswordManagerGUI()
    window.show()
    sys.exit(app.exec_())
