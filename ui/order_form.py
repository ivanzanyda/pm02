from PyQt6.QtWidgets import (
    QDialog, QLabel, QComboBox, QSpinBox, QPushButton, QTableWidget,
    QLineEdit, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget
)


class Ui_OrderFormDialog:
    def setupUi(self, OrderFormDialog):
        OrderFormDialog.resize(800, 600)
        OrderFormDialog.setWindowTitle('Создание заказа')

        main = QVBoxLayout(OrderFormDialog)

        self.frameSelectItem = QWidget()
        select = QGridLayout(self.frameSelectItem)
        self.labelMenuItem = QLabel('Позиция')
        self.comboBoxMenuItem = QComboBox()
        self.labelQuantity = QLabel('Количество')
        self.spinBoxQuantity = QSpinBox()
        self.spinBoxQuantity.setMinimum(1)
        self.pushButtonAddItem = QPushButton('Добавить')
        select.addWidget(self.labelMenuItem, 0, 0)
        select.addWidget(self.comboBoxMenuItem, 0, 1)
        select.addWidget(self.labelQuantity, 0, 2)
        select.addWidget(self.spinBoxQuantity, 0, 3)
        select.addWidget(self.pushButtonAddItem, 0, 4)
        main.addWidget(self.frameSelectItem)

        self.tableWidgetOrderItems = QTableWidget(0, 5)
        self.tableWidgetOrderItems.setHorizontalHeaderLabels(['ID', 'Название', 'Кол-во', 'Цена', 'Сумма'])
        main.addWidget(self.tableWidgetOrderItems)

        self.frameOrderInfo = QWidget()
        info = QGridLayout(self.frameOrderInfo)
        self.labelOrderType = QLabel('Тип заказа')
        self.comboBoxOrderType = QComboBox()
        self.labelAddress = QLabel('Адрес')
        self.lineEditDeliveryAddress = QLineEdit()
        self.labelComment = QLabel('Комментарий')
        self.plainTextEditComment = QPlainTextEdit()
        info.addWidget(self.labelOrderType, 0, 0)
        info.addWidget(self.comboBoxOrderType, 0, 1)
        info.addWidget(self.labelAddress, 1, 0)
        info.addWidget(self.lineEditDeliveryAddress, 1, 1)
        info.addWidget(self.labelComment, 2, 0)
        info.addWidget(self.plainTextEditComment, 2, 1)
        main.addWidget(self.frameOrderInfo)

        self.frameBottom = QWidget()
        bottom = QHBoxLayout(self.frameBottom)
        self.labelTotalCaption = QLabel('Итоговая сумма:')
        self.labelTotalAmount = QLabel('0.00 ₽')
        self.pushButtonSaveOrder = QPushButton('Сохранить')
        self.pushButtonCancel = QPushButton('Отмена')
        bottom.addWidget(self.labelTotalCaption)
        bottom.addWidget(self.labelTotalAmount)
        bottom.addStretch()
        bottom.addWidget(self.pushButtonSaveOrder)
        bottom.addWidget(self.pushButtonCancel)
        main.addWidget(self.frameBottom)
