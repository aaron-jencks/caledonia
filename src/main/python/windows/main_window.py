from typing import Callable
from queue import Queue, Full
import os.path as path
import os

from PySide2 import QtCore
from PySide2.QtWidgets import QLabel, QTreeView, QVBoxLayout, QHBoxLayout, QPushButton, \
    QFileSystemModel, QFileDialog, QCheckBox, QSpinBox, QTextEdit, QLCDNumber, QComboBox
from PySide2.QtCore import Slot, QDir, Qt

from windows.base import Window
from settings import algorithm_directory


class ToggleButton:
    def __init__(self, frame_text: str, checkbox_text: str = 'Default'):
        self.box = QVBoxLayout()
        self.lbl = QLabel(frame_text)

        self.checkbox = QCheckBox(checkbox_text)
        self.checkbox.setCheckState(Qt.Unchecked)

        self.numeric = QSpinBox()
        self.numeric.setValue(-1)

        self.box.addWidget(self.lbl)
        self.box.addWidget(self.numeric)
        self.box.addWidget(self.checkbox)

        self.checkbox.stateChanged.connect(self.checkbox_toggle)
        self.numeric.valueChanged.connect(self.numeric_change)

        self.use_default = False
        self.value = -1

    @Slot()
    def checkbox_toggle(self, checked):
        self.use_default = self.checkbox.checkState() == Qt.Checked
        self.numeric.setDisabled(self.use_default)

    @Slot()
    def numeric_change(self, checked):
        self.value = self.numeric.value()


class TestController(Window):
    """Contains code for  the window that the user initially sees"""

    def __init__(self):
        if not path.exists(algorithm_directory):
            os.makedirs(algorithm_directory, exist_ok=True)

        self.fmodel = QFileSystemModel()
        self.fmodel.setRootPath(algorithm_directory)
        self.module_list = QTreeView()
        self.module_list.setModel(self.fmodel)
        self.module_list.setRootIndex(self.fmodel.index(algorithm_directory))
        self.module_button = QPushButton("Change Directory")
        self.module_button.clicked.connect(self.change_dir)

        self.start_date = ToggleButton('Start Date')
        self.end_date = ToggleButton('End Date', 'Default (Present)')

        self.test_types = ['Profit', 'Accuracy']
        self.test_type = QComboBox()
        self.test_type.addItems(self.test_types)

        self.test_output = QTextEdit()
        self.test_output.setDisabled(True)
        self.run_btn = QPushButton('Run Test')

        self.profit = QLCDNumber()
        self.accuracy = QLCDNumber()

        super().__init__('Jencks Stock Algorithm Tester')

    def setup_left_column(self):
        self.left.addWidget(QLabel("Test Files"))
        self.left.addWidget(self.module_list)
        self.left.addWidget(self.module_button)

    def setup_center_column(self):
        hbox = QHBoxLayout()
        hbox.addLayout(self.start_date.box)
        hbox.addLayout(self.end_date.box)
        self.center.addLayout(hbox)
        self.center.addWidget(QLabel('Test Type'))
        self.center.addWidget(self.test_type)
        self.center.addWidget(QLabel('Test Run Output'))
        self.center.addWidget(self.test_output)
        self.center.addWidget(self.run_btn)

    def setup_right_column(self):
        self.right.addWidget(QLabel('Test Diagnostics'))
        self.right.addWidget(QLabel('Profit'))
        self.right.addWidget(self.profit)
        self.right.addWidget(QLabel('Accuracy'))
        self.right.addWidget(self.accuracy)

    def setup_menus(self):
        super().setup_menus()
        self.menu_entries += [
            (self.edit_menu, 'Preferences', self.open_preferences, 'Ctrl+Alt+P')
        ]

    @Slot()
    def open_preferences(self, checked):
        print('Opening preference menu.')

    @Slot()
    def change_dir(self, checked):
        dialog = QFileDialog()
        fdir = dialog.getExistingDirectory()
        self.fmodel.setRootPath(fdir)
        self.module_list.setRootIndex(self.fmodel.index(fdir))
