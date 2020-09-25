from typing import Callable
from PySide2.QtWidgets import QMainWindow, QApplication, QAction, QMenuBar, QHBoxLayout, QVBoxLayout, QLabel, QWidget
from PySide2.QtCore import Slot


class Window(QMainWindow):
    """Contains code for  the window that the user initially sees"""

    def __init__(self, title: str = ''):
        super().__init__()
        self.setWindowTitle(title)

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.edit_menu = self.menu.addMenu("Edit")

        self.menu_entries = []
        self.setup_menus()
        for entry in self.menu_entries:
            m, n, t, sh = entry
            self.add_menu_entry(m, n, t, sh)

        self.widget = QWidget()

        self.left = QVBoxLayout()
        self.setup_left_column()
        self.center = QVBoxLayout()
        self.setup_center_column()
        self.right = QVBoxLayout()
        self.setup_right_column()

        self.columns = QHBoxLayout()
        self.columns.addLayout(self.left)
        self.columns.addLayout(self.center)
        self.columns.addLayout(self.right)

        self.widget.setLayout(self.columns)
        self.setCentralWidget(self.widget)

    def setup_left_column(self):
        self.left.addWidget(QLabel("This is the left column"))
        pass

    def setup_center_column(self):
        self.center.addWidget(QLabel("This is the center column"))
        pass

    def setup_right_column(self):
        self.right.addWidget(QLabel("This is the right column"))
        pass

    def setup_menus(self):
        self.menu_entries += [
            (self.file_menu, 'Exit', self.exit_app, 'Ctrl+Q')
        ]

    def add_menu_entry(self, menu: QMenuBar,
                       name: str, trigger: Callable, shortcut: str = ''):
        action = QAction(name, self)

        if len(shortcut) > 0:
            action.setShortcut(shortcut)

        action.triggered.connect(trigger)

        menu.addAction(action)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()
