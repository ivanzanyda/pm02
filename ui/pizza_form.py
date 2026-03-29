from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QComboBox, QDoubleSpinBox, QPushButton,
    QPlainTextEdit, QVBoxLayout, QGridLayout, QWidget, QHBoxLayout
)


class Ui_PizzaFormDialog:
    def setupUi(self, PizzaFormDialog):
        PizzaFormDialog.resize(520, 420)
        PizzaFormDialog.setWindowTitle('Позиция меню')

        main = QVBoxLayout(PizzaFormDialog)

        form = QWidget()
        grid = QGridLayout(form)
        self.labelName = QLabel('Название')
        self.lineEditName = QLineEdit()
        self.labelPrice = QLabel('Цена')
        self.doubleSpinBoxPrice = QDoubleSpinBox()
        self.doubleSpinBoxPrice.setMaximum(100000)
        self.doubleSpinBoxPrice.setDecimals(2)
        self.labelCategory = QLabel('Категория')
        self.comboBoxCategory = QComboBox()
        self.labelOffer = QLabel('Акция')
        self.comboBoxOffer = QComboBox()
        self.labelImage = QLabel('Картинка')
        self.lineEditImage = QLineEdit()
        self.pushButtonBrowseImage = QPushButton('Обзор')
        grid.addWidget(self.labelName, 0, 0)
        grid.addWidget(self.lineEditName, 0, 1, 1, 2)
        grid.addWidget(self.labelPrice, 1, 0)
        grid.addWidget(self.doubleSpinBoxPrice, 1, 1, 1, 2)
        grid.addWidget(self.labelCategory, 2, 0)
        grid.addWidget(self.comboBoxCategory, 2, 1, 1, 2)
        grid.addWidget(self.labelOffer, 3, 0)
        grid.addWidget(self.comboBoxOffer, 3, 1, 1, 2)
        grid.addWidget(self.labelImage, 4, 0)
        grid.addWidget(self.lineEditImage, 4, 1)
        grid.addWidget(self.pushButtonBrowseImage, 4, 2)
        main.addWidget(form)

        self.labelDescription = QLabel('Описание')
        self.plainTextEditDescription = QPlainTextEdit()
        main.addWidget(self.labelDescription)
        main.addWidget(self.plainTextEditDescription)

        buttons = QHBoxLayout()
        buttons.addStretch()
        self.pushButtonSave = QPushButton('Сохранить')
        self.pushButtonCancel = QPushButton('Отмена')
        buttons.addWidget(self.pushButtonSave)
        buttons.addWidget(self.pushButtonCancel)
        main.addLayout(buttons)
