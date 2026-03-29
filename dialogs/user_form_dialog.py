from PyQt6.QtWidgets import QDialog, QMessageBox

from database.db import all_roles, one_user, add_user, edit_user
from ui.user_form import Ui_UserFormDialog


class UserFormDialog(QDialog, Ui_UserFormDialog):
    def __init__(self, user_id=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.pushButtonSave.clicked.connect(self.save_data)
        self.pushButtonCancel.clicked.connect(self.reject)

        self.comboBoxRole.clear()
        for role in all_roles():
            self.comboBoxRole.addItem(role['role_name'], role['id'])

        if self.user_id:
            self.load_user_data()

    def load_user_data(self):
        user = one_user(self.user_id)
        if not user:
            self.reject()
            return

        self.lineEditUsername.setText(user['username'])
        self.lineEditPassword.setText(user['password'])
        self.lineEditFullName.setText(user['full_name'])
        self.lineEditContact.setText(user['contact_info'] or '')

        index = self.comboBoxRole.findData(user['role_id'])
        if index >= 0:
            self.comboBoxRole.setCurrentIndex(index)

    def save_data(self):
        username = self.lineEditUsername.text().strip()
        password = self.lineEditPassword.text().strip()
        full_name = self.lineEditFullName.text().strip()
        contact = self.lineEditContact.text().strip()
        role_id = self.comboBoxRole.currentData()

        if not username or not password or not full_name:
            QMessageBox.warning(self, 'Ошибка', 'Заполните обязательные поля')
            return

        ok = edit_user(self.user_id, username, password, full_name, contact, role_id) if self.user_id else add_user(username, password, full_name, contact, role_id)
        if ok:
            self.accept()
