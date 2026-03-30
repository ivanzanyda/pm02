from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDialog, QMessageBox

from database.db import one_offer, add_offer, edit_offer
from ui.offer_form import Ui_OfferFormDialog


class OfferFormDialog(QDialog, Ui_OfferFormDialog):
    def __init__(self, offer_id=None):
        super().__init__()
        self.setupUi(self)

        self.offer_id = offer_id
        self.dateEditFrom.setDate(QDate.currentDate())
        self.dateEditTo.setDate(QDate.currentDate())

        self.pushButtonSave.clicked.connect(self.save_data)
        self.pushButtonCancel.clicked.connect(self.reject)

        if self.offer_id:
            self.load_offer_data()

    def load_offer_data(self):
        offer = one_offer(self.offer_id)
        if not offer:
            self.reject()
            return

        self.lineEditName.setText(offer['name'])
        self.plainTextEditDescription.setPlainText(offer['description'] or '')
        self.doubleSpinBoxDiscount.setValue(float(offer['discount_percentage']))
        self.dateEditFrom.setDate(QDate.fromString(str(offer['valid_from']), 'yyyy-MM-dd'))
        self.dateEditTo.setDate(QDate.fromString(str(offer['valid_to']), 'yyyy-MM-dd'))

    def save_data(self):
        name = self.lineEditName.text().strip()
        description = self.plainTextEditDescription.toPlainText().strip()
        discount = self.doubleSpinBoxDiscount.value()
        valid_from = self.dateEditFrom.date().toPyDate()
        valid_to = self.dateEditTo.date().toPyDate()

        if not name:
            QMessageBox.warning(self, 'Ошибка', 'Введите название')
            return

        ok = edit_offer(self.offer_id, name, description, discount, valid_from, valid_to) if self.offer_id else add_offer(name, description, discount, valid_from, valid_to)
        if ok:
            self.accept()
