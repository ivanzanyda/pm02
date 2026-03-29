from PyQt6.QtWidgets import QMainWindow, QMessageBox

from database.db import check_login
from ui.login import Ui_LoginWindow
from users.admin import admin_window
from users.client import client_window
from users.guest import guest_window
from users.manager import manager_window
from users.operator import operator_window


class login_window(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButtonLogin.clicked.connect(self.login)
        self.pushButtonGuest.clicked.connect(self.open_guest)
        self.pushButtonExit.clicked.connect(self.close)

    def login(self):
        username = self.lineEditLogin.text().strip()
        password = self.lineEditPassword.text().strip()

        if not username or not password:
            self.labelStatus.setText('Введите логин и пароль')
            QMessageBox.warning(self, 'Ошибка', 'Введите логин и пароль')
            return

        user = check_login(username, password)
        if not user:
            self.labelStatus.setText('Неверный логин или пароль')
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')
            return

        role = user['role']
        if role == 'client':
            self.win = client_window(user['id'], user['full_name'])
        elif role == 'operator':
            self.win = operator_window(user['full_name'])
        elif role == 'manager':
            self.win = manager_window(user['full_name'])
        elif role == 'admin':
            self.win = admin_window(user['full_name'])
        else:
            QMessageBox.warning(self, 'Ошибка', f'Неизвестная роль: {role}')
            return

        self.win.show()
        self.close()

    def open_guest(self):
        self.win = guest_window()
        self.win.show()
        self.close()
