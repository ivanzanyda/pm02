import sys
from PyQt6.QtWidgets import QApplication
from auth.auth import login_window

app = QApplication(sys.argv)
window = login_window()
window.show()
sys.exit(app.exec())
