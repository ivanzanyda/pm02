from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTabWidget, QScrollArea, QTableWidget, QStatusBar
)


class Ui_ManagerWindow:
    def setupUi(self, ManagerWindow):
        ManagerWindow.resize(1200, 760)
        ManagerWindow.setWindowTitle('Пиццерия — Менеджер')

        self.centralwidget = QWidget(ManagerWindow)
        ManagerWindow.setCentralWidget(self.centralwidget)
        main = QVBoxLayout(self.centralwidget)

        self.frameTop = QWidget()
        top = QHBoxLayout(self.frameTop)
        self.labelWindowTitle = QLabel('Рабочее место менеджера')
        self.labelCurrentUser = QLabel('Менеджер')
        self.pushButtonLogout = QPushButton('Выйти')
        top.addWidget(self.labelWindowTitle)
        top.addStretch()
        top.addWidget(self.labelCurrentUser)
        top.addWidget(self.pushButtonLogout)
        main.addWidget(self.frameTop)

        self.tabWidgetMain = QTabWidget()
        main.addWidget(self.tabWidgetMain)

        self.tabCatalog = QWidget()
        catalog = QVBoxLayout(self.tabCatalog)
        self.frameCatalogActions = QWidget()
        cat_buttons = QHBoxLayout(self.frameCatalogActions)
        self.pushButtonRefreshMenu = QPushButton('Обновить меню')
        self.pushButtonAddPizza = QPushButton('Добавить')
        self.pushButtonEditPizza = QPushButton('Редактировать')
        self.pushButtonDeletePizza = QPushButton('Удалить')
        self.pushButtonChangePrice = QPushButton('Изменить цену')
        for w in [self.pushButtonRefreshMenu, self.pushButtonAddPizza, self.pushButtonEditPizza, self.pushButtonDeletePizza, self.pushButtonChangePrice]:
            cat_buttons.addWidget(w)
        cat_buttons.addStretch()
        catalog.addWidget(self.frameCatalogActions)
        self.scrollAreaCatalog = QScrollArea()
        self.scrollAreaCatalog.setWidgetResizable(True)
        self.scrollAreaWidgetContentsCatalog = QWidget()
        self.scrollAreaCatalog.setWidget(self.scrollAreaWidgetContentsCatalog)
        catalog.addWidget(self.scrollAreaCatalog)
        self.tabWidgetMain.addTab(self.tabCatalog, 'Ассортимент')

        self.tabOffers = QWidget()
        offers = QVBoxLayout(self.tabOffers)
        self.frameOffersButtons = QWidget()
        offer_buttons = QHBoxLayout(self.frameOffersButtons)
        self.pushButtonRefreshOffers = QPushButton('Обновить')
        self.pushButtonAddOffer = QPushButton('Добавить')
        self.pushButtonEditOffer = QPushButton('Редактировать')
        self.pushButtonDeleteOffer = QPushButton('Удалить')
        for w in [self.pushButtonRefreshOffers, self.pushButtonAddOffer, self.pushButtonEditOffer, self.pushButtonDeleteOffer]:
            offer_buttons.addWidget(w)
        offer_buttons.addStretch()
        offers.addWidget(self.frameOffersButtons)
        self.tableWidgetOffers = QTableWidget(0, 5)
        self.tableWidgetOffers.setHorizontalHeaderLabels(['ID', 'Название', 'Скидка', 'Дата с', 'Дата по'])
        offers.addWidget(self.tableWidgetOffers)
        self.tabWidgetMain.addTab(self.tabOffers, 'Акции')

        self.statusbar = QStatusBar(ManagerWindow)
        ManagerWindow.setStatusBar(self.statusbar)
