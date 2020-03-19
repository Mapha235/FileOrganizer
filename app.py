from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QFileDialog, QGridLayout, QSizePolicy, QWidget, QTextBrowser
import sys
from stylesheets import *


class TheWindow(QWidget):
    def __init__(self):
        super(TheWindow, self).__init__()
        self.x = 960
        self.y = 200
        self.my_width = 800
        self.my_height = 500

        # set Background Image
        self.bg = QImage("C:/Dev/python/FileOrganizer/data/bg.png")

        self.settings_button = QtWidgets.QPushButton(self)
        self.create_entry_button = QtWidgets.QPushButton("Create new entry", self)
        self.run_script_button = QtWidgets.QPushButton(self)

        #list of all buttons
        self.buttons = []

        self.buttons.append(self.settings_button)
        self.buttons.append(self.create_entry_button)
        self.buttons.append(self.run_script_button)

        self.source_text_browser = QTextBrowser()
        self.target_text_browser = QTextBrowser()
        self.keyword_text_browser = QTextBrowser()

        # create Text Fields
        self.text_fields = []

        self.text_fields.append(self.source_text_browser)
        self.text_fields.append(self.target_text_browser)
        self.text_fields.append(self.keyword_text_browser)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("File Organizer")
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)

        # Design of the settings button
        self.settings_button.setFixedSize(70, 70)
        self.settings_button.setIcon(QtGui.QIcon("C:/Dev/python/FileOrganizer/data/Settings.png"))
        self.settings_button.setIconSize(QtCore.QSize(60, 60))

        self.run_script_button.setFixedSize(70, 70)
        self.run_script_button.setIcon(QtGui.QIcon("C:/Dev/python/FileOrganizer/data/arrow.png"))
        self.run_script_button.setIconSize(QtCore.QSize(60, 60))

        self.create_entry_button.setFixedHeight(70)

        for button, text in zip(self.buttons, self.text_fields):
            # used for mouse hover event
            button.installEventFilter(self)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            # assign design layout to all widgets
            text.setStyleSheet(layout1)

        self.createGridLayout()

    def createGridLayout(self):
        layout_grid = QGridLayout()

        self.setLayout(layout_grid)
        layout_grid.setSpacing(10)

        layout_grid.addWidget(self.settings_button, 0, 0, 1, 1)
        layout_grid.addWidget(self.create_entry_button, 0, 1, 1, 8)

        layout_grid.addWidget(self.keyword_text_browser, 1, 0, 1, 9)

        layout_grid.addWidget(self.source_text_browser, 2, 0, 1, 4)
        layout_grid.addWidget(self.run_script_button, 2, 4, 1, 1)
        layout_grid.addWidget(self.target_text_browser, 2, 5, 1, 4)

    def eventFilter(self, obj, event):
        button = obj

        if event.type() == QtCore.QEvent.HoverEnter:
            self.onHovered(button)
        elif event.type() == QtCore.QEvent.HoverLeave:
            self.update()

        return super(TheWindow, self).eventFilter(obj, event)

    def onHovered(self, btn):
        btn.setStyleSheet(mouse_hover)

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName(self)
        print(filename)

    def my_print(self):
        print(self.height)

    def update(self):
        size = self.size()

        self.my_width = size.width()
        self.my_height = size.height()

        # set background image
        scaled_bg = self.bg.scaled(QSize(self.my_width, self.my_height))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(scaled_bg))
        self.setPalette(palette)

        self.settings_button.setStyleSheet(layout1)
        self.create_entry_button.setStyleSheet(layout1)
        self.run_script_button.setStyleSheet(layout1)

    def resizeEvent(self, event):
        self.update()


def window():
    app = QApplication(sys.argv)
    win = TheWindow()

    win.show()
    sys.exit(app.exec_())


