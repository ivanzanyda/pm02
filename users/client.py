from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidgetItem, QMessageBox, QInputDialog

from database.db import all_menu_items, one_menu_item, orders_by_user, one_order, edit_order, delete_order, reviews_by_user
from dialogs.order_form_dialog import OrderFormDialog
from dialogs.review_form_dialog import ReviewFormDialog
from ui.client_win import Ui_ClientWindow
from users.pizza_card import PizzaCard


class client_window(QMainWindow, Ui_ClientWindow):
    def __init__(self, user_id, full_name=''):
        super().__init__()
        self.setupUi(self)

        self.user_id = user_id
        self.labelCurrentUser.setText(full_name or 'Клиент')
        self.images_dir = Path(__file__).resolve().parent.parent / 'resources' / 'images'

        self.comboBoxOrderStatusFilter.addItems([
            'Все', 'Ожидает приготовления', 'Готовится', 'Готово',
            'Доставляется', 'Выдан', 'Отменен'
        ])

        self.pushButtonLogout.clicked.connect(self.back_to_login)
        self.pushButtonRefreshMenu.clicked.connect(self.load_menu)
        self.pushButtonCreateOrder.clicked.connect(self.open_order_form)
        self.pushButtonAddComment.clicked.connect(self.add_order_comment)
        self.pushButtonRefreshOrders.clicked.connect(self.load_orders)
        self.pushButtonDeleteOrder.clicked.connect(self.delete_selected_order)
        self.comboBoxOrderStatusFilter.currentTextChanged.connect(self.load_orders)
        self.pushButtonNewReview.clicked.connect(self.open_review_form)
        self.pushButtonAskQuestion.clicked.connect(self.ask_question)
        self.pushButtonRefreshReviews.clicked.connect(self.load_reviews)

        self.cards_widget = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_widget)
        self.cards_layout.setContentsMargins(10, 10, 10, 10)
        self.cards_layout.setSpacing(10)
        self.scrollAreaCatalog.setWidget(self.cards_widget)
        self.scrollAreaCatalog.setWidgetResizable(True)

        self.load_menu()
        self.load_orders()
        self.load_reviews()

    def clear_cards(self):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_menu(self):
        self.clear_cards()
        for item in all_menu_items():
            card = PizzaCard(item, self.images_dir)
            card.clicked.connect(self.show_item_info)
            self.cards_layout.addWidget(card)
        self.cards_layout.addStretch()

    def show_item_info(self, item_id):
        item = one_menu_item(item_id)
        if not item:
            return
        text = (
            f"Название: {item['name']}\n"
            f"Категория: {item['category']}\n"
            f"Цена: {float(item['price']):.2f} ₽\n\n"
            f"Описание:\n{item['description'] or 'Нет описания'}"
        )
        QMessageBox.information(self, 'Позиция меню', text)

    def load_orders(self):
        rows = orders_by_user(self.user_id)
        status = self.comboBoxOrderStatusFilter.currentText()
        if status != 'Все':
            rows = [row for row in rows if row['status'] == status]

        self.tableWidgetOrders.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tableWidgetOrders.setItem(i, 0, QTableWidgetItem(str(row['order_id'])))
            self.tableWidgetOrders.setItem(i, 1, QTableWidgetItem(str(row['order_date'])))
            self.tableWidgetOrders.setItem(i, 2, QTableWidgetItem(str(row['order_type'])))
            self.tableWidgetOrders.setItem(i, 3, QTableWidgetItem(str(row['delivery_address'] or '')))
            self.tableWidgetOrders.setItem(i, 4, QTableWidgetItem(str(row['customer_comment'] or '')))
            self.tableWidgetOrders.setItem(i, 5, QTableWidgetItem(str(row['total_amount'])))
            self.tableWidgetOrders.setItem(i, 6, QTableWidgetItem(str(row['status'])))

    def get_selected_order_id(self):
        row = self.tableWidgetOrders.currentRow()
        if row < 0:
            return None
        item = self.tableWidgetOrders.item(row, 0)
        return int(item.text()) if item else None

    def open_order_form(self):
        dialog = OrderFormDialog(self.user_id, self)
        if dialog.exec():
            self.load_orders()

    def add_order_comment(self):
        order_id = self.get_selected_order_id()
        if not order_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите заказ')
            return

        order = one_order(order_id)
        if not order:
            return

        text, ok = QInputDialog.getMultiLineText(
            self, 'Комментарий', 'Введите комментарий:', order['customer_comment'] or ''
        )
        if not ok:
            return

        if edit_order(
            order_id,
            order['order_type'],
            order['delivery_address'],
            text.strip(),
            order['total_amount'],
            order['status']
        ):
            self.load_orders()

    def delete_selected_order(self):
        order_id = self.get_selected_order_id()
        if not order_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите заказ')
            return

        order = one_order(order_id)
        if not order:
            return

        if order['status'] != 'Ожидает приготовления':
            QMessageBox.warning(self, 'Ошибка', 'Можно удалить только новый заказ')
            return

        if delete_order(order_id):
            self.load_orders()

    def load_reviews(self):
        rows = reviews_by_user(self.user_id)
        self.tableWidgetReviews.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tableWidgetReviews.setItem(i, 0, QTableWidgetItem(str(row['item_name'])))
            self.tableWidgetReviews.setItem(i, 1, QTableWidgetItem(str(row['rating'])))
            self.tableWidgetReviews.setItem(i, 2, QTableWidgetItem(str(row['comment'] or '')))
            self.tableWidgetReviews.setItem(i, 3, QTableWidgetItem(str(row['review_date'])))

    def open_review_form(self):
        dialog = ReviewFormDialog(self.user_id, self)
        if dialog.exec():
            self.load_reviews()

    def ask_question(self):
        order_id = self.get_selected_order_id()
        if not order_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите заказ')
            return

        text, ok = QInputDialog.getMultiLineText(self, 'Вопрос', 'Введите вопрос:')
        if not ok or not text.strip():
            return

        order = one_order(order_id)
        if not order:
            return

        comment = (order['customer_comment'] or '').strip()
        if comment:
            comment += '\n'
        comment += 'Вопрос клиента: ' + text.strip()

        if edit_order(
            order_id,
            order['order_type'],
            order['delivery_address'],
            comment,
            order['total_amount'],
            order['status']
        ):
            self.plainTextEditQuestionPreview.setPlainText(text.strip())
            self.load_orders()

    def back_to_login(self):
        from auth.auth import login_window
        self.win = login_window()
        self.win.show()
        self.close()
