from PyQt5 import QtWidgets
from stylesheets import *

class Entry(QtWidgets):
    def __init__(self):
        self.target_button = QtWidgets.QPushButton(self)
        self.source_button = QtWidgets.QPushButton("Browse", self)
        self.setStyleSheet(font)



    def initUI(self):
        buttons = []
        self.source_button.setFixedHeight(50)
        self.source_button.clicked.connect(self.open_dialog_box)
        buttons.append(self.source_button)

        self.target_button.setFixedHeight(50)
        self.target_button.clicked.connect(self.open_dialog_box)
        buttons.append(self.target_button)