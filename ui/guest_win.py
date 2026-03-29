from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QStatusBar


class Ui_GuestWindow:
    def setupUi(self, GuestWindow):
        GuestWindow.resize(1000, 700)
        GuestWindow.setWindowTitle('Пиццерия - гость')

        self.centralwidget = QWidget(GuestWindow)
        GuestWindow.setCentralWidget(self.centralwidget)

        main = QVBoxLayout(self.centralwidget)

        self.frameTop = QWidget()
        top = QHBoxLayout(self.frameTop)
        self.labelWindowTitle = QLabel('Каталог меню')
        self.labelUserCaption = QLabel('Пользователь:')
        self.labelCurrentUser = QLabel('Гость')
        self.pushButtonBackToLogin = QPushButton('К авторизации')
        self.pushButtonRefreshMenu = QPushButton('Обновить меню')
        top.addWidget(self.labelWindowTitle)
        top.addStretch()
        top.addWidget(self.labelUserCaption)
        top.addWidget(self.labelCurrentUser)
        top.addWidget(self.pushButtonBackToLogin)
        top.addWidget(self.pushButtonRefreshMenu)
        main.addWidget(self.frameTop)

        self.labelHint = QLabel('Гость может только смотреть меню')
        main.addWidget(self.labelHint)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        main.addWidget(self.scrollArea)

        self.statusbar = QStatusBar(GuestWindow)
        GuestWindow.setStatusBar(self.statusbar)
