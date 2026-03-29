from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox

from database.db import all_menu_items, one_menu_item
from ui.guest_win import Ui_GuestWindow
from users.pizza_card import PizzaCard


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
        self.cards_layout.setContentsMargins(10, 10, 10, 10)
        self.cards_layout.setSpacing(10)
        self.scrollArea.setWidget(self.cards_widget)
        self.scrollArea.setWidgetResizable(True)

        self.load_menu()

    def clear_cards(self):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_menu(self):
        self.items = all_menu_items()
        self.clear_cards()

        for item in self.items:
            card = PizzaCard(item, self.images_dir)
            card.clicked.connect(self.show_item_info)
            self.cards_layout.addWidget(card)

        self.cards_layout.addStretch()
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

        QMessageBox.information(self, 'Позиция меню', text)

    def back_to_login(self):
        from auth.auth import login_window
        self.win = login_window()
        self.win.show()
        self.close()
