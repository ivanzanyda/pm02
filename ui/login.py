from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QStatusBar


class Ui_LoginWindow:
    def setupUi(self, LoginWindow):
        LoginWindow.resize(420, 240)
        LoginWindow.setWindowTitle('Авторизация')

        self.centralwidget = QWidget(LoginWindow)
        LoginWindow.setCentralWidget(self.centralwidget)

        layout = QVBoxLayout(self.centralwidget)

        self.label = QLabel('Пиццерия - авторизация')
        layout.addWidget(self.label)

        self.lineEditLogin = QLineEdit()
        self.lineEditLogin.setPlaceholderText('Логин')
        layout.addWidget(self.lineEditLogin)

        self.lineEditPassword = QLineEdit()
        self.lineEditPassword.setPlaceholderText('Пароль')
        self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.lineEditPassword)

        self.labelStatus = QLabel('')
        layout.addWidget(self.labelStatus)

        buttons = QHBoxLayout()
        self.pushButtonLogin = QPushButton('Войти')
        self.pushButtonGuest = QPushButton('Войти как гость')
        self.pushButtonExit = QPushButton('Выход')
        buttons.addWidget(self.pushButtonLogin)
        buttons.addWidget(self.pushButtonGuest)
        buttons.addWidget(self.pushButtonExit)
        layout.addLayout(buttons)

        self.statusbar = QStatusBar(LoginWindow)
        LoginWindow.setStatusBar(self.statusbar)
