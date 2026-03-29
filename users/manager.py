from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidgetItem, QMessageBox, QInputDialog

from database.db import all_menu_items, one_menu_item, delete_menu_item, edit_menu_item, all_offers, delete_offer
from dialogs.offer_form_dialog import OfferFormDialog
from dialogs.pizza_form_dialog import PizzaFormDialog
from ui.manager_win import Ui_ManagerWindow
from users.pizza_card import PizzaCard


class manager_window(QMainWindow, Ui_ManagerWindow):
    def __init__(self, full_name=''):
        super().__init__()
        self.setupUi(self)

        self.labelCurrentUser.setText(full_name or 'Менеджер')
        self.images_dir = Path(__file__).resolve().parent.parent / 'resources' / 'images'
        self.selected_item_id = None

        self.pushButtonLogout.clicked.connect(self.back_to_login)
        self.pushButtonRefreshMenu.clicked.connect(self.load_menu)
        self.pushButtonAddPizza.clicked.connect(self.add_pizza)
        self.pushButtonEditPizza.clicked.connect(self.edit_pizza)
        self.pushButtonDeletePizza.clicked.connect(self.delete_pizza)
        self.pushButtonChangePrice.clicked.connect(self.change_price)
        self.pushButtonRefreshOffers.clicked.connect(self.load_offers)
        self.pushButtonAddOffer.clicked.connect(self.add_offer_dialog)
        self.pushButtonEditOffer.clicked.connect(self.edit_offer_dialog)
        self.pushButtonDeleteOffer.clicked.connect(self.delete_offer_dialog)

        self.cards_widget = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_widget)
        self.cards_layout.setContentsMargins(10, 10, 10, 10)
        self.cards_layout.setSpacing(10)
        self.scrollAreaCatalog.setWidget(self.cards_widget)
        self.scrollAreaCatalog.setWidgetResizable(True)

        self.load_menu()
        self.load_offers()

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
            card.clicked.connect(self.select_item)
            self.cards_layout.addWidget(card)
        self.cards_layout.addStretch()

    def select_item(self, item_id):
        self.selected_item_id = item_id
        item = one_menu_item(item_id)
        if item:
            self.statusbar.showMessage(f"Выбрана позиция: {item['name']}")

    def add_pizza(self):
        dialog = PizzaFormDialog(parent=self)
        if dialog.exec():
            self.load_menu()

    def edit_pizza(self):
        if not self.selected_item_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите карточку')
            return
        dialog = PizzaFormDialog(self.selected_item_id, self)
        if dialog.exec():
            self.load_menu()

    def delete_pizza(self):
        if not self.selected_item_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите карточку')
            return
        if delete_menu_item(self.selected_item_id):
            self.selected_item_id = None
            self.load_menu()

    def change_price(self):
        if not self.selected_item_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите карточку')
            return

        item = one_menu_item(self.selected_item_id)
        if not item:
            return

        price, ok = QInputDialog.getDouble(self, 'Цена', 'Новая цена:', float(item['price']), 0, 100000, 2)
        if ok and edit_menu_item(
            self.selected_item_id,
            item['name'],
            item['description'],
            price,
            item['category'],
            item['image'],
            item['offer_id']
        ):
            self.load_menu()

    def load_offers(self):
        rows = all_offers()
        self.tableWidgetOffers.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tableWidgetOffers.setItem(i, 0, QTableWidgetItem(str(row['id'])))
            self.tableWidgetOffers.setItem(i, 1, QTableWidgetItem(str(row['name'])))
            self.tableWidgetOffers.setItem(i, 2, QTableWidgetItem(str(row['discount_percentage'])))
            self.tableWidgetOffers.setItem(i, 3, QTableWidgetItem(str(row['valid_from'])))
            self.tableWidgetOffers.setItem(i, 4, QTableWidgetItem(str(row['valid_to'])))

    def get_selected_offer_id(self):
        row = self.tableWidgetOffers.currentRow()
        if row < 0:
            return None
        item = self.tableWidgetOffers.item(row, 0)
        return int(item.text()) if item else None

    def add_offer_dialog(self):
        dialog = OfferFormDialog(parent=self)
        if dialog.exec():
            self.load_offers()

    def edit_offer_dialog(self):
        offer_id = self.get_selected_offer_id()
        if not offer_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите акцию')
            return
        dialog = OfferFormDialog(offer_id, self)
        if dialog.exec():
            self.load_offers()

    def delete_offer_dialog(self):
        offer_id = self.get_selected_offer_id()
        if not offer_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите акцию')
            return
        if delete_offer(offer_id):
            self.load_offers()

    def back_to_login(self):
        from auth.auth import login_window
        self.win = login_window()
        self.win.show()
        self.close()
