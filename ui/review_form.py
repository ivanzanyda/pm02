from PyQt6.QtWidgets import QDialog, QLabel, QComboBox, QSpinBox, QPlainTextEdit, QPushButton, QVBoxLayout, QGridLayout, QWidget, QHBoxLayout


class Ui_ReviewFormDialog:
    def setupUi(self, ReviewFormDialog):
        ReviewFormDialog.resize(500, 320)
        ReviewFormDialog.setWindowTitle('Отзыв')

        main = QVBoxLayout(ReviewFormDialog)

        form = QWidget()
        grid = QGridLayout(form)
        self.labelMenuItem = QLabel('Пицца')
        self.comboBoxMenuItem = QComboBox()
        self.labelRating = QLabel('Оценка')
        self.spinBoxRating = QSpinBox()
        self.spinBoxRating.setMinimum(1)
        self.spinBoxRating.setMaximum(5)
        grid.addWidget(self.labelMenuItem, 0, 0)
        grid.addWidget(self.comboBoxMenuItem, 0, 1)
        grid.addWidget(self.labelRating, 1, 0)
        grid.addWidget(self.spinBoxRating, 1, 1)
        main.addWidget(form)

        self.labelComment = QLabel('Комментарий')
        self.plainTextEditComment = QPlainTextEdit()
        main.addWidget(self.labelComment)
        main.addWidget(self.plainTextEditComment)

        buttons = QHBoxLayout()
        buttons.addStretch()
        self.pushButtonSave = QPushButton('Сохранить')
        self.pushButtonCancel = QPushButton('Отмена')
        buttons.addWidget(self.pushButtonSave)
        buttons.addWidget(self.pushButtonCancel)
        main.addLayout(buttons)
