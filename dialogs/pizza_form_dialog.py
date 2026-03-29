from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt6.QtCore import QDate
import os

from database.db import all_categories, all_offers, one_menu_item, add_menu_item, edit_menu_item
from ui.pizza_form import Ui_PizzaFormDialog


class PizzaFormDialog(QDialog, Ui_PizzaFormDialog):
    def __init__(self, item_id=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.item_id = item_id
        self.pushButtonSave.clicked.connect(self.save_data)
        self.pushButtonCancel.clicked.connect(self.reject)
        self.pushButtonBrowseImage.clicked.connect(self.browse_image)

        self.load_categories()
        self.load_offers()

        if self.item_id:
            self.load_item_data()

    def load_categories(self):
        self.comboBoxCategory.clear()
        categories = all_categories() or ['Пицца', 'Закуска', 'Десерт', 'Напиток']
        for category in categories:
            self.comboBoxCategory.addItem(category)

    def load_offers(self):
        self.comboBoxOffer.clear()
        self.comboBoxOffer.addItem('Нет акции', None)
        for offer in all_offers():
            self.comboBoxOffer.addItem(offer['name'], offer['id'])

    def load_item_data(self):
        item = one_menu_item(self.item_id)
        if not item:
            QMessageBox.warning(self, 'Ошибка', 'Позиция не найдена')
            self.reject()
            return

        self.lineEditName.setText(item['name'])
        self.plainTextEditDescription.setPlainText(item['description'] or '')
        self.doubleSpinBoxPrice.setValue(float(item['price']))
        self.lineEditImage.setText(item['image'] or '')
        self.comboBoxCategory.setCurrentText(item['category'])

        index = self.comboBoxOffer.findData(item['offer_id'])
        if index >= 0:
            self.comboBoxOffer.setCurrentIndex(index)

    def browse_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Выберите картинку', '', 'Images (*.png *.jpg *.jpeg *.webp)')
        if file_name:
            self.lineEditImage.setText(os.path.basename(file_name))

    def save_data(self):
        name = self.lineEditName.text().strip()
        description = self.plainTextEditDescription.toPlainText().strip()
        price = self.doubleSpinBoxPrice.value()
        category = self.comboBoxCategory.currentText().strip()
        image = self.lineEditImage.text().strip()
        offer_id = self.comboBoxOffer.currentData()

        if not name:
            QMessageBox.warning(self, 'Ошибка', 'Введите название')
            return

        ok = edit_menu_item(self.item_id, name, description, price, category, image, offer_id) if self.item_id else add_menu_item(name, description, price, category, image, offer_id)
        if ok:
            self.accept()
