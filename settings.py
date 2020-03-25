from PyQt5 import QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.QtWidgets import QWidget, QTextBrowser, QVBoxLayout


class Settings(QWidget):
    def __init__(self, x, y):
        super(Settings, self).__init__()
        self.x = x
        self.y = y
        self.my_width = 400
        self.my_height = 430

        self.container = QtWidgets.QGroupBox()
        self.initUI()

    def initUI(self):
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)
        self.createGridLayout()

    def createGridLayout(self):
        layout = QVBoxLayout(self.container)
        layout.setSpacing(10)
        self.setLayout(layout)


