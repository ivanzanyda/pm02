from PyQt6.QtWidgets import QDialog, QMessageBox

from database.db import all_menu_items, add_review
from ui.review_form import Ui_ReviewFormDialog


class ReviewFormDialog(QDialog, Ui_ReviewFormDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.pushButtonSave.clicked.connect(self.save_data)
        self.pushButtonCancel.clicked.connect(self.reject)

        self.comboBoxMenuItem.clear()
        for item in all_menu_items():
            self.comboBoxMenuItem.addItem(item['name'], item['item_id'])

    def save_data(self):
        item_id = self.comboBoxMenuItem.currentData()
        rating = self.spinBoxRating.value()
        comment = self.plainTextEditComment.toPlainText().strip()

        if not comment:
            QMessageBox.warning(self, 'Ошибка', 'Введите комментарий')
            return

        if add_review(self.user_id, item_id, rating, comment):
            self.accept()
