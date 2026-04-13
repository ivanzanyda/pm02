from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox

from database.db import all_menu_items, one_menu_item
from ui.guest_win import Ui_GuestWindow
from users.pizza_card import pizza_card


class guest_window(QMainWindow, Ui_GuestWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.images_dir = Path(__file__).resolve().parent.parent / 'resources' / 'images'
        self.items = []

        self.pushButtonBackToLogin.clicked.connect(self.back_to_login)
        self.pushButtonRefreshMenu.clicked.connect(self.load_menu)

        self.cards_widget = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_widget)
        self.scrollArea.setWidget(self.cards_widget)

        self.load_menu()

    def load_menu(self):
        self.items = all_menu_items()

        for item in self.items:
            card = pizza_card(item, self.images_dir)
            card.clicked.connect(self.show_item_info)
            self.cards_layout.addWidget(card)
        self.statusbar.showMessage(f'Загружено позиций: {len(self.items)}')

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
        if item.get('discount_percentage'):
            text += f"\n\nСкидка: {float(item['discount_percentage']):g}%"

        QMessageBox.information(self, item.get('name'), text)

    def back_to_login(self):
        from auth.auth import login_window
        self.win = login_window()
        self.win.show()
        self.close()
