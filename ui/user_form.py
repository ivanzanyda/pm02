from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QGridLayout, QWidget, QHBoxLayout


class Ui_UserFormDialog:
    def setupUi(self, UserFormDialog):
        UserFormDialog.resize(500, 320)
        UserFormDialog.setWindowTitle('Пользователь')

        main = QVBoxLayout(UserFormDialog)

        form = QWidget()
        grid = QGridLayout(form)
        self.labelUsername = QLabel('Логин')
        self.lineEditUsername = QLineEdit()
        self.labelPassword = QLabel('Пароль')
        self.lineEditPassword = QLineEdit()
        self.labelFullName = QLabel('ФИО')
        self.lineEditFullName = QLineEdit()
        self.labelContact = QLabel('Контакты')
        self.lineEditContact = QLineEdit()
        self.labelRole = QLabel('Роль')
        self.comboBoxRole = QComboBox()
        grid.addWidget(self.labelUsername, 0, 0)
        grid.addWidget(self.lineEditUsername, 0, 1)
        grid.addWidget(self.labelPassword, 1, 0)
        grid.addWidget(self.lineEditPassword, 1, 1)
        grid.addWidget(self.labelFullName, 2, 0)
        grid.addWidget(self.lineEditFullName, 2, 1)
        grid.addWidget(self.labelContact, 3, 0)
        grid.addWidget(self.lineEditContact, 3, 1)
        grid.addWidget(self.labelRole, 4, 0)
        grid.addWidget(self.comboBoxRole, 4, 1)
        main.addWidget(form)

        buttons = QHBoxLayout()
        buttons.addStretch()
        self.pushButtonSave = QPushButton('Сохранить')
        self.pushButtonCancel = QPushButton('Отмена')
        buttons.addWidget(self.pushButtonSave)
        buttons.addWidget(self.pushButtonCancel)
        main.addLayout(buttons)
