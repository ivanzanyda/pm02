from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout


class PizzaCard(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, item, images_dir):
        super().__init__()

        self.item_id = item["item_id"]

        self.setFrameShape(QFrame.Shape.Box)
        self.setMinimumHeight(170)

        layout = QHBoxLayout(self)

        labelImage = QLabel()
        labelImage.setFixedSize(170, 140)
        labelImage.setFrameShape(QFrame.Shape.Box)
        labelImage.setScaledContents(True)

        image_name = item.get("image") or ""
        image_path = Path(images_dir) / image_name if image_name else None

        if image_path:
            labelImage.setPixmap(QPixmap(str(image_path)))
        else:
            labelImage.setText("Нет фото")

        labelInfo = QLabel()

        category = item.get("category", "")
        name = item.get("name", "")
        description = item.get("description", "") or "Нет описания"
        price = float(item.get("price", 0))
        discount = item.get("discount_percentage")

        if discount:
            discount = float(discount)
            new_price = price - price * discount / 100
            price_text = (
                f"Цена: <span style='color:red; text-decoration:line-through;'>"
                f"{price:.2f} ₽</span> {new_price:.2f} ₽"
            )
            discount_text = f"Скидка\n{discount:g}%"
        else:
            price_text = f"Цена: <b>{price:.2f} ₽</b>"
            discount_text = "Скидки\nнет"

        labelInfo.setText(
            f"{category} | {name}<br>"
            f"Описание: {description}<br>"
            f"{price_text}"
        )

        labelDiscount = QLabel(discount_text)
        labelDiscount.setFixedWidth(100)
        labelDiscount.setFrameShape(QFrame.Shape.Box)
        labelDiscount.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(labelImage)
        layout.addWidget(labelInfo, 1)
        layout.addWidget(labelDiscount)

    def mousePressEvent(self, event):
        self.clicked.emit(self.item_id)
        super().mousePressEvent(event)
