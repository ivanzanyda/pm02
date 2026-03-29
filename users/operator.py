from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox

from database.db import all_orders, filter_orders_status, update_order_status
from ui.operator_win import Ui_OperatorWindow


class operator_window(QMainWindow, Ui_OperatorWindow):
    def __init__(self, full_name=''):
        super().__init__()
        self.setupUi(self)

        self.labelCurrentUser.setText(full_name or 'Оператор')
        self.dateEditFrom.setDate(QDate.currentDate())
        self.dateEditTo.setDate(QDate.currentDate())

        self.comboBoxStatusFilter.addItems([
            'Все', 'Ожидает приготовления', 'Готовится', 'Готово',
            'Доставляется', 'Выдан', 'Отменен'
        ])
        self.comboBoxNewStatus.addItems([
            'Ожидает приготовления', 'Готовится', 'Готово',
            'Доставляется', 'Выдан', 'Отменен'
        ])

        self.pushButtonLogout.clicked.connect(self.back_to_login)
        self.pushButtonApplyFilters.clicked.connect(self.load_orders)
        self.pushButtonRefreshOrders.clicked.connect(self.load_orders)
        self.pushButtonUpdateStatus.clicked.connect(self.change_status)
        self.tableWidgetOrders.itemSelectionChanged.connect(self.set_selected_order)

        self.load_orders()

    def load_orders(self):
        rows = all_orders() if self.comboBoxStatusFilter.currentText() == 'Все' else filter_orders_status(self.comboBoxStatusFilter.currentText())
        date_from = self.dateEditFrom.date().toPyDate()
        date_to = self.dateEditTo.date().toPyDate()
        rows = [row for row in rows if date_from <= (row['order_date'].date() if hasattr(row['order_date'], 'date') else row['order_date']) <= date_to]

        self.tableWidgetOrders.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tableWidgetOrders.setItem(i, 0, QTableWidgetItem(str(row['order_id'])))
            self.tableWidgetOrders.setItem(i, 1, QTableWidgetItem(str(row['full_name'])))
            self.tableWidgetOrders.setItem(i, 2, QTableWidgetItem(str(row['order_date'])))
            self.tableWidgetOrders.setItem(i, 3, QTableWidgetItem(str(row['order_type'])))
            self.tableWidgetOrders.setItem(i, 4, QTableWidgetItem(str(row['delivery_address'] or '')))
            self.tableWidgetOrders.setItem(i, 5, QTableWidgetItem(str(row['customer_comment'] or '')))
            self.tableWidgetOrders.setItem(i, 6, QTableWidgetItem(str(row['total_amount'])))
            self.tableWidgetOrders.setItem(i, 7, QTableWidgetItem(str(row['status'])))

    def set_selected_order(self):
        row = self.tableWidgetOrders.currentRow()
        if row < 0:
            return
        item = self.tableWidgetOrders.item(row, 0)
        if item:
            self.lineEditSelectedOrderId.setText(item.text())

    def change_status(self):
        order_id = self.lineEditSelectedOrderId.text().strip()
        if not order_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите заказ')
            return

        if update_order_status(int(order_id), self.comboBoxNewStatus.currentText()):
            self.load_orders()

    def back_to_login(self):
        from auth.auth import login_window
        self.win = login_window()
        self.win.show()
        self.close()
