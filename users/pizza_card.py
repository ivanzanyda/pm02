from pathlib import Path
from PyQt6.QtWidgets import QFrame,QLabel,QHBoxLayout
from PyQt6.QtCore import Qt,pyqtSignal
from PyQt6.QtGui import QPixmap

class pizza_card(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, item,path_dir):
        super().__init__()

        self.item_id = item['item_id']

        self.setFrameShape(QFrame.Shape.Box)
        self.setMinimumHeight(170)

        layout = QHBoxLayout(self)

        label_image = QLabel()
        label_image.setFrameShape(QFrame.Shape.Box)
        label_image.setFixedSize(170,170)
        label_image.setScaledContents(True)

        image_name = item.get('name')
        image_path = Path(path_dir) / image_name

        if image_path:
            label_image.setPixmap(QPixmap(str(image_path)))
        else:
            label_image.setText('Нет фото')

        label_info = QLabel()

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
        
        label_info.setText(
            f"{category} | {name}<br>"
            f"описание: {description}<br>"
            f"{price_text}"
        )

        label_discount = QLabel(discount_text)
        label_discount.setFrameShape(QFrame.Shape.Box)
        label_discount.setMaximumSize(50,50)
        label_discount.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label_image)
        layout.addWidget(label_info)
        layout.addWidget(label_discount)

    def mousePressEvent(self, event):
        self.clicked.emit(self.item_id)
        super().mousePressEvent(event)

        