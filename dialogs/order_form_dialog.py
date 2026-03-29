from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox

from database.db import all_menu_items, add_order, add_order_item
from ui.order_form import Ui_OrderFormDialog


class OrderFormDialog(QDialog, Ui_OrderFormDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.current_items = []

        self.comboBoxOrderType.addItems(['В зале', 'Навынос', 'Доставка'])
        self.pushButtonAddItem.clicked.connect(self.add_item_to_order)
        self.pushButtonSaveOrder.clicked.connect(self.save_order)
        self.pushButtonCancel.clicked.connect(self.reject)

        self.load_menu_items()

    def load_menu_items(self):
        self.comboBoxMenuItem.clear()
        for item in all_menu_items():
            self.comboBoxMenuItem.addItem(item['name'], item)

    def add_item_to_order(self):
        item = self.comboBoxMenuItem.currentData()
        if not item:
            return

        quantity = self.spinBoxQuantity.value()
        self.current_items.append({
            'item_id': item['item_id'],
            'name': item['name'],
            'quantity': quantity,
            'unit_price': float(item['price']),
            'amount': float(item['price']) * quantity
        })
        self.fill_items_table()
        self.update_total()

    def fill_items_table(self):
        self.tableWidgetOrderItems.setRowCount(len(self.current_items))
        for i, item in enumerate(self.current_items):
            self.tableWidgetOrderItems.setItem(i, 0, QTableWidgetItem(str(item['item_id'])))
            self.tableWidgetOrderItems.setItem(i, 1, QTableWidgetItem(item['name']))
            self.tableWidgetOrderItems.setItem(i, 2, QTableWidgetItem(str(item['quantity'])))
            self.tableWidgetOrderItems.setItem(i, 3, QTableWidgetItem(f"{item['unit_price']:.2f}"))
            self.tableWidgetOrderItems.setItem(i, 4, QTableWidgetItem(f"{item['amount']:.2f}"))

    def update_total(self):
        total = sum(item['amount'] for item in self.current_items)
        self.labelTotalAmount.setText(f'{total:.2f} ₽')

    def save_order(self):
        if not self.current_items:
            QMessageBox.warning(self, 'Ошибка', 'Добавьте позицию')
            return

        order_type = self.comboBoxOrderType.currentText()
        address = self.lineEditDeliveryAddress.text().strip()
        comment = self.plainTextEditComment.toPlainText().strip()
        total = sum(item['amount'] for item in self.current_items)

        if order_type == 'Доставка' and not address:
            QMessageBox.warning(self, 'Ошибка', 'Введите адрес')
            return

        order_id = add_order(self.user_id, order_type, address, comment, total)
        if not order_id:
            QMessageBox.warning(self, 'Ошибка', 'Не удалось сохранить заказ')
            return

        for item in self.current_items:
            add_order_item(order_id, item['item_id'], item['quantity'], item['unit_price'])

        self.accept()
