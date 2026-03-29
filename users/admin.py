from pathlib import Path

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidgetItem, QMessageBox, QInputDialog

from database.db import (
    all_users, delete_user, all_menu_items, one_menu_item, delete_menu_item,
    all_orders, filter_orders_status, update_order_status,
    total_orders_sum, orders_status_stats, popular_items,
    all_roles, add_role, edit_role, delete_role
)
from dialogs.pizza_form_dialog import PizzaFormDialog
from dialogs.user_form_dialog import UserFormDialog
from ui.admin_win import Ui_AdminWindow
from users.pizza_card import PizzaCard


class admin_window(QMainWindow, Ui_AdminWindow):
    def __init__(self, full_name=''):
        super().__init__()
        self.setupUi(self)

        self.labelCurrentUser.setText(full_name or 'Администратор')
        self.images_dir = Path(__file__).resolve().parent.parent / 'resources' / 'images'
        self.selected_item_id = None

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
        self.pushButtonRefreshUsers.clicked.connect(self.load_users)
        self.pushButtonAddUser.clicked.connect(self.add_user_dialog)
        self.pushButtonEditUser.clicked.connect(self.edit_user_dialog)
        self.pushButtonDeleteUser.clicked.connect(self.delete_user_dialog)
        self.pushButtonRefreshMenu.clicked.connect(self.load_menu)
        self.pushButtonAddPizza.clicked.connect(self.add_pizza_dialog)
        self.pushButtonEditPizza.clicked.connect(self.edit_pizza_dialog)
        self.pushButtonDeletePizza.clicked.connect(self.delete_pizza_dialog)
        self.pushButtonOpenOffers.clicked.connect(lambda: QMessageBox.information(self, 'Акции', 'Акциями управляет менеджер'))
        self.pushButtonApplyOrderFilters.clicked.connect(self.load_orders)
        self.pushButtonRefreshOrders.clicked.connect(self.load_orders)
        self.pushButtonUpdateStatus.clicked.connect(self.change_status)
        self.pushButtonRefreshAnalytics.clicked.connect(self.load_analytics)
        self.pushButtonGenerateReport.clicked.connect(self.generate_report)
        self.pushButtonRefreshRoles.clicked.connect(self.load_roles_table)
        self.pushButtonAddRole.clicked.connect(self.add_role_dialog)
        self.pushButtonEditRole.clicked.connect(self.edit_role_dialog)
        self.pushButtonDeleteRole.clicked.connect(self.delete_role_dialog)
        self.tableWidgetOrders.itemSelectionChanged.connect(self.set_selected_order)

        self.cards_widget = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_widget)
        self.cards_layout.setContentsMargins(10, 10, 10, 10)
        self.cards_layout.setSpacing(10)
        self.scrollAreaMenu.setWidget(self.cards_widget)
        self.scrollAreaMenu.setWidgetResizable(True)

        self.load_users()
        self.load_menu()
        self.load_orders()
        self.load_analytics()
        self.load_roles_table()

    def clear_cards(self):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    # users
    def load_users(self):
        rows = all_users()
        self.tableWidgetUsers.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tableWidgetUsers.setItem(i, 0, QTableWidgetItem(str(row['id'])))
            self.tableWidgetUsers.setItem(i, 1, QTableWidgetItem(str(row['username'])))
            self.tableWidgetUsers.setItem(i, 2, QTableWidgetItem(str(row['password'])))
            self.tableWidgetUsers.setItem(i, 3, QTableWidgetItem(str(row['full_name'])))
            self.tableWidgetUsers.setItem(i, 4, QTableWidgetItem(str(row['contact_info'] or '')))
            self.tableWidgetUsers.setItem(i, 5, QTableWidgetItem(str(row['role'])))

    def get_selected_user_id(self):
        row = self.tableWidgetUsers.currentRow()
        if row < 0:
            return None
        item = self.tableWidgetUsers.item(row, 0)
        return int(item.text()) if item else None

    def add_user_dialog(self):
        dialog = UserFormDialog(parent=self)
        if dialog.exec():
            self.load_users()

    def edit_user_dialog(self):
        user_id = self.get_selected_user_id()
        if not user_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите пользователя')
            return
        dialog = UserFormDialog(user_id, self)
        if dialog.exec():
            self.load_users()

    def delete_user_dialog(self):
        user_id = self.get_selected_user_id()
        if not user_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите пользователя')
            return
        if delete_user(user_id):
            self.load_users()

    # menu
    def load_menu(self):
        self.clear_cards()
        for item in all_menu_items():
            card = PizzaCard(item, self.images_dir)
            card.clicked.connect(self.select_item)
            self.cards_layout.addWidget(card)
        self.cards_layout.addStretch()

    def select_item(self, item_id):
        self.selected_item_id = item_id
        item = one_menu_item(item_id)
        if item:
            self.statusbar.showMessage(f"Выбрана позиция: {item['name']}")

    def add_pizza_dialog(self):
        dialog = PizzaFormDialog(parent=self)
        if dialog.exec():
            self.load_menu()

    def edit_pizza_dialog(self):
        if not self.selected_item_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите карточку')
            return
        dialog = PizzaFormDialog(self.selected_item_id, self)
        if dialog.exec():
            self.load_menu()

    def delete_pizza_dialog(self):
        if not self.selected_item_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите карточку')
            return
        if delete_menu_item(self.selected_item_id):
            self.selected_item_id = None
            self.load_menu()

    # orders
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

    # analytics
    def load_analytics(self):
        self.labelTotalSalesValue.setText(f"{float(total_orders_sum()['total_sum']):.2f} ₽")

        rows = orders_status_stats()
        self.tableWidgetStatusStats.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tableWidgetStatusStats.setItem(i, 0, QTableWidgetItem(str(row['status'])))
            self.tableWidgetStatusStats.setItem(i, 1, QTableWidgetItem(str(row['total_count'])))

        rows = popular_items()
        self.tableWidgetPopularPizzas.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tableWidgetPopularPizzas.setItem(i, 0, QTableWidgetItem(str(row['name'])))
            self.tableWidgetPopularPizzas.setItem(i, 1, QTableWidgetItem(str(row['total_quantity'])))
            self.tableWidgetPopularPizzas.setItem(i, 2, QTableWidgetItem(str(row['total_amount'])))

    def generate_report(self):
        QMessageBox.information(self, 'Отчет', f"Общая сумма: {self.labelTotalSalesValue.text()}")

    # roles
    def load_roles_table(self):
        rows = all_roles()
        self.tableWidgetRoles.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tableWidgetRoles.setItem(i, 0, QTableWidgetItem(str(row['id'])))
            self.tableWidgetRoles.setItem(i, 1, QTableWidgetItem(str(row['role_name'])))

    def get_selected_role_id(self):
        row = self.tableWidgetRoles.currentRow()
        if row < 0:
            return None
        item = self.tableWidgetRoles.item(row, 0)
        return int(item.text()) if item else None

    def add_role_dialog(self):
        text, ok = QInputDialog.getText(self, 'Роль', 'Название роли:')
        if ok and text.strip() and add_role(text.strip()):
            self.load_roles_table()

    def edit_role_dialog(self):
        role_id = self.get_selected_role_id()
        if not role_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите роль')
            return
        current = self.tableWidgetRoles.item(self.tableWidgetRoles.currentRow(), 1).text()
        text, ok = QInputDialog.getText(self, 'Роль', 'Новое название:', text=current)
        if ok and text.strip() and edit_role(role_id, text.strip()):
            self.load_roles_table()

    def delete_role_dialog(self):
        role_id = self.get_selected_role_id()
        if not role_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите роль')
            return
        if delete_role(role_id):
            self.load_roles_table()

    def back_to_login(self):
        from auth.auth import login_window
        self.win = login_window()
        self.win.show()
        self.close()
