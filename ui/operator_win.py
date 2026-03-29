from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QDateEdit, QComboBox, QTableWidget, QLineEdit, QStatusBar
)


class Ui_OperatorWindow:
    def setupUi(self, OperatorWindow):
        OperatorWindow.resize(1200, 760)
        OperatorWindow.setWindowTitle('Пиццерия — Оператор')

        self.centralwidget = QWidget(OperatorWindow)
        OperatorWindow.setCentralWidget(self.centralwidget)
        main = QVBoxLayout(self.centralwidget)

        self.frameTop = QWidget()
        top = QHBoxLayout(self.frameTop)
        self.labelWindowTitle = QLabel('Оператор кухни')
        self.labelCurrentUser = QLabel('Оператор')
        self.pushButtonLogout = QPushButton('Выйти')
        top.addWidget(self.labelWindowTitle)
        top.addStretch()
        top.addWidget(self.labelCurrentUser)
        top.addWidget(self.pushButtonLogout)
        main.addWidget(self.frameTop)

        self.frameFilters = QWidget()
        filters = QGridLayout(self.frameFilters)
        self.labelDateFrom = QLabel('Дата с')
        self.dateEditFrom = QDateEdit()
        self.dateEditFrom.setCalendarPopup(True)
        self.labelDateTo = QLabel('Дата по')
        self.dateEditTo = QDateEdit()
        self.dateEditTo.setCalendarPopup(True)
        self.labelStatusFilter = QLabel('Статус')
        self.comboBoxStatusFilter = QComboBox()
        self.pushButtonApplyFilters = QPushButton('Применить')
        self.pushButtonRefreshOrders = QPushButton('Обновить')
        filters.addWidget(self.labelDateFrom, 0, 0)
        filters.addWidget(self.dateEditFrom, 0, 1)
        filters.addWidget(self.labelDateTo, 0, 2)
        filters.addWidget(self.dateEditTo, 0, 3)
        filters.addWidget(self.labelStatusFilter, 0, 4)
        filters.addWidget(self.comboBoxStatusFilter, 0, 5)
        filters.addWidget(self.pushButtonApplyFilters, 0, 6)
        filters.addWidget(self.pushButtonRefreshOrders, 0, 7)
        main.addWidget(self.frameFilters)

        self.tableWidgetOrders = QTableWidget(0, 8)
        self.tableWidgetOrders.setHorizontalHeaderLabels(['ID', 'Клиент', 'Дата', 'Тип', 'Адрес', 'Комментарий', 'Сумма', 'Статус'])
        main.addWidget(self.tableWidgetOrders)

        self.frameStatus = QWidget()
        status = QHBoxLayout(self.frameStatus)
        self.labelSelectedOrder = QLabel('Выбранный заказ')
        self.lineEditSelectedOrderId = QLineEdit()
        self.labelNewStatus = QLabel('Новый статус')
        self.comboBoxNewStatus = QComboBox()
        self.pushButtonUpdateStatus = QPushButton('Изменить статус')
        status.addWidget(self.labelSelectedOrder)
        status.addWidget(self.lineEditSelectedOrderId)
        status.addWidget(self.labelNewStatus)
        status.addWidget(self.comboBoxNewStatus)
        status.addWidget(self.pushButtonUpdateStatus)
        main.addWidget(self.frameStatus)

        self.statusbar = QStatusBar(OperatorWindow)
        OperatorWindow.setStatusBar(self.statusbar)
