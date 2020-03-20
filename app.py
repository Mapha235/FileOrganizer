import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QGridLayout, QSizePolicy, QWidget, QTextBrowser

from entry import Entry
from stylesheets import *


class TheWindow(QWidget):
    def __init__(self):
        super(TheWindow, self).__init__()
        self.x = -1160
        self.y = 200
        self.my_width = 800
        self.my_height = 500

        self.entry = None

        # set Background Image
        self.bg = QImage("./data/bg.png")

        self.settings_button = QtWidgets.QPushButton(self)
        self.create_entry_button = QtWidgets.QPushButton("Create new entry", self)
        self.run_script_button = QtWidgets.QPushButton(self)

        # list of all buttons
        self.buttons = []

        self.buttons.append(self.settings_button)
        self.buttons.append(self.create_entry_button)
        self.buttons.append(self.run_script_button)

        self.source_text_browser = QTextBrowser(self)
        self.target_text_browser = QTextBrowser(self)
        self.entry_text_browser = QTextBrowser(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("File Organizer")
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)
        self.setMinimumSize(800, 500)

        # Design of the settings button
        self.settings_button.setFixedSize(70, 70)
        self.settings_button.setIcon(
            QtGui.QIcon("./data/Settings.png"))
        self.settings_button.setIconSize(QtCore.QSize(60, 60))

        self.run_script_button.setFixedWidth(70)
        self.run_script_button.setIcon(
            QtGui.QIcon("./data/arrow.png"))
        self.run_script_button.setIconSize(QtCore.QSize(60, 60))

        self.create_entry_button.setFixedHeight(70)

        for button in self.buttons:
            # used for mouse hover event
            button.installEventFilter(self)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.buttons.clear()

        # assign design layout to all widgets
        self.setStyleSheet(layout1)
        self.createGridLayout()

    def createGridLayout(self):
        layout_grid = QGridLayout()

        self.setLayout(layout_grid)
        layout_grid.setSpacing(10)

        layout_grid.addWidget(self.settings_button, 0, 0, 1, 1)
        layout_grid.addWidget(self.create_entry_button, 0, 1, 1, 8)

        layout_grid.addWidget(self.entry_text_browser, 1, 0, 1, 9)

        layout_grid.addWidget(self.source_text_browser, 2, 0, 1, 4)
        layout_grid.addWidget(self.run_script_button, 2, 4, 1, 1)
        layout_grid.addWidget(self.target_text_browser, 2, 5, 1, 4)

    def openEntry(self):
        self.entry = Entry(self.pos().x() + (self.width() / 4), self.pos().y() + 50)
        self.entry.show()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            obj.setStyleSheet(mouse_hover)
        elif event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
            obj.setStyleSheet(mouse_hover + mouse_click)
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            obj.setStyleSheet(mouse_hover)
            if obj == self.create_entry_button:
                self.openEntry()
        elif event.type() == QtCore.QEvent.HoverLeave:
            obj.setStyleSheet(layout1)
        return super(TheWindow, self).eventFilter(obj, event)

    def resizeBg(self):
        self.my_width = self.width()
        self.my_height = self.height()

        # set background image
        scaled_bg = self.bg.scaled(QSize(self.my_width, self.my_height))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(scaled_bg))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.resizeBg()


def window():
    app = QApplication(sys.argv)
    win = TheWindow()
    win.show()
    sys.exit(app.exec_())
