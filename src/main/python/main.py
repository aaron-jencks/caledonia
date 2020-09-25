from PySide2.QtWidgets import QApplication
from windows.main_window import TestController

import sys

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestController()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())
