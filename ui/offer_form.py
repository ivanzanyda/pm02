from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QDateEdit, QDoubleSpinBox, QPushButton,
    QPlainTextEdit, QVBoxLayout, QGridLayout, QWidget, QHBoxLayout
)


class Ui_OfferFormDialog:
    def setupUi(self, OfferFormDialog):
        OfferFormDialog.resize(500, 360)
        OfferFormDialog.setWindowTitle('Акция')

        main = QVBoxLayout(OfferFormDialog)

        form = QWidget()
        grid = QGridLayout(form)
        self.labelName = QLabel('Название')
        self.lineEditName = QLineEdit()
        self.labelDiscount = QLabel('Скидка')
        self.doubleSpinBoxDiscount = QDoubleSpinBox()
        self.doubleSpinBoxDiscount.setMaximum(100)
        self.labelDateFrom = QLabel('Дата с')
        self.dateEditFrom = QDateEdit()
        self.dateEditFrom.setCalendarPopup(True)
        self.labelDateTo = QLabel('Дата по')
        self.dateEditTo = QDateEdit()
        self.dateEditTo.setCalendarPopup(True)
        grid.addWidget(self.labelName, 0, 0)
        grid.addWidget(self.lineEditName, 0, 1)
        grid.addWidget(self.labelDiscount, 1, 0)
        grid.addWidget(self.doubleSpinBoxDiscount, 1, 1)
        grid.addWidget(self.labelDateFrom, 2, 0)
        grid.addWidget(self.dateEditFrom, 2, 1)
        grid.addWidget(self.labelDateTo, 3, 0)
        grid.addWidget(self.dateEditTo, 3, 1)
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
